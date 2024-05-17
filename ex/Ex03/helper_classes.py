import numpy as np

epsilon = 1e-6


# This function gets a vector and returns its normalized form.
def normalize(vector):
    return vector / np.linalg.norm(vector)


# This function gets a vector and the normal of the surface it hit
# This function returns the vector that reflects from the surface
def reflected(vector, axis):
    return normalize(vector - 2 * np.dot(vector, axis) * axis)



## Lights

class LightSource:
    def __init__(self, intensity):
        self.intensity = intensity


class DirectionalLight(LightSource):

    def __init__(self, intensity, direction):
        super().__init__(intensity)
        self.direction = normalize(direction)

    # This function returns the ray that goes from the light source to a point
    def get_light_ray(self, intersection_point):
        return Ray(intersection_point, (-1) * self.direction)


    # This function returns the distance from a point to the light source
    def get_distance_from_light(self, intersection):
        return np.inf

    # This function returns the light intensity at a point
    def get_intensity(self, intersection):
        return self.intensity


class PointLight(LightSource):
    def __init__(self, intensity, position, kc, kl, kq):
        super().__init__(intensity)
        self.position = np.array(position)
        self.kc = kc
        self.kl = kl
        self.kq = kq

    # This function returns the ray that goes from a point to the light source
    def get_light_ray(self, intersection):
        return Ray(intersection, normalize(self.position - intersection))

    # This function returns the distance from a point to the light source
    def get_distance_from_light(self, intersection):
        return np.linalg.norm(intersection - self.position)

    # This function returns the light intensity at a point
    def get_intensity(self, intersection):
        d = self.get_distance_from_light(intersection)
        return self.intensity / (self.kc + self.kl * d + self.kq * (d ** 2))


class SpotLight(LightSource):
    def __init__(self, intensity, position, direction, kc, kl, kq):
        super().__init__(intensity)
        self.position = np.array(position)
        self.direction = direction
        self.kc = kc
        self.kl = kl
        self.kq = kq

    # This function returns the ray that goes from a point to the light source
    def get_light_ray(self, intersection):
        return Ray(intersection, normalize(self.position - self.direction))

    def get_distance_from_light(self, intersection):
        return np.linalg.norm(intersection - self.position)

    def get_intensity(self, intersection):
        distance_from_light = self.get_distance_from_light(intersection)
        direction_to_point = normalize(intersection - self.position)
        dot_product = np.dot(direction_to_point, normalize(self.direction))
        return (self.intensity * dot_product) / (self.kc + self.kl * distance_from_light + self.kq *
                                                 (distance_from_light ** 2))


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = normalize(direction)

    # The function is getting the collection of objects in the scene and looks for the one with minimum distance.
    # The function should return the nearest object and its distance (in two different arguments)
    def nearest_intersected_object(self, objects):
        intersection_point = None
        nearest_object = None
        min_t = np.inf

        for obj in objects:
            t, intersected_object = obj.intersect(self)
            if t is not None and min_t > t > epsilon:
                min_t = t
                nearest_object = intersected_object
                intersection_point = self.origin + t * self.direction
        return nearest_object, min_t, intersection_point



class Object3D:
    def __init__(self):
        self.material = None

    def set_material(self, ambient, diffuse, specular, shininess, reflection):
        self.material = {
            'ambient': ambient,  ## Ka
            'diffuse': diffuse,  ## Kd
            'specular': specular,  ## Ks
            'shininess': shininess,  ## n
            'reflection': reflection  ## Kr
        }


class Plane(Object3D):
    def __init__(self, normal, point):
        super().__init__()
        self.normal = np.array(normal)
        self.point = np.array(point)

    def intersect(self, ray: Ray):
        denominator = np.dot(self.normal, ray.direction)
        if abs(denominator) < epsilon:
            return None, None
        v = self.point - ray.origin
        t = np.dot(v, self.normal) / denominator
        if t > 0:
            return t, self
        return None, None


class Triangle(Object3D):
    # """
    #     C
    #     /\
    #    /  \
    # A /____\ B
    #
    # The fornt face of the triangle is A -> B -> C.
    #
    # """

    def __init__(self, a, b, c):
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)
        self.normal = self.compute_normal()

    # computes normal to the trainagle surface. Pay attention to its direction!
    def compute_normal(self):
        ba = self.a - self.b
        bc = self.c - self.b
        return normalize(np.cross(bc, ba))

    def intersect(self, ray):
        ab = self.b - self.a
        ac = self.c - self.a
        A = np.column_stack((ab, ac, -ray.direction))
        if np.linalg.det(A) == 0:
            return None, None
        b = ray.origin - self.a
        try:
            # Solving the system using numpy's linear algebra solver
            u, v, t = np.linalg.solve(A, b)
            # Check if the solution is within the bounds of the triangle and ray is pointing towards it
            if epsilon <= u <= 1 and epsilon <= v <= 1 and (u + v) <= 1 and t > epsilon:
                return t, self
            else:
                return None, None
        except np.linalg.LinAlgError:
            # This occurs if the matrix A is singular, i.e., no solution
            return None, None


class Pyramid(Object3D):
    #     """
    #             D
    #             /\*\
    #            /==\**\
    #          /======\***\
    #        /==========\***\
    #      /==============\****\
    #    /==================\*****\
    # A /&&&&&&&&&&&&&&&&&&&&\ B &&&/ C
    #    \==================/****/
    #      \==============/****/
    #        \==========/****/
    #          \======/***/
    #            \==/**/
    #             \/*/
    #              E
    #
    #     Similar to Traingle, every from face of the diamond's faces are:
    #         A -> B -> D
    #         B -> C -> D
    #         A -> C -> B
    #         E -> B -> A
    #         E -> C -> B
    #         C -> E -> A
    #     """

    def __init__(self, v_list):
        self.v_list = v_list
        self.triangle_list = self.create_triangle_list()

    def create_triangle_list(self):
        l = []
        t_idx = [
            [0, 1, 3],
            [1, 2, 3],
            [0, 3, 2],
            [4, 1, 0],
            [4, 2, 1],
            [2, 4, 0]
        ]
        for idx in t_idx:
            a = self.v_list[idx[0]]
            b = self.v_list[idx[1]]
            c = self.v_list[idx[2]]
            l.append(Triangle(a, b, c))
        return l

    def apply_materials_to_triangles(self):
        for triangle in self.triangle_list:
            triangle.set_material(self.material["ambient"], self.material["diffuse"], self.material["specular"],
                                  self.material["shininess"], self.material["reflection"])

    def intersect(self, ray: Ray):
        intersection = ray.nearest_intersected_object(self.triangle_list)
        if intersection is not None:
            nearest_object, min_t, _ = intersection
            return min_t, nearest_object
        return None, None


class Sphere(Object3D):
    def __init__(self, center, radius: float):
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray):
        # a = np.dot(ray.direction, ray.direction)
        # b = 2 * np.dot(ray.direction, ray.origin - self.center)
        # c = np.dot(ray.origin - self.center, ray.origin - self.center) - self.radius ** 2
        # discriminant = b ** 2 - 4 * a * c
        # if discriminant < 0:
        #     return None, None
        # t1 = (-b + np.sqrt(discriminant)) / (2 * a)
        # t2 = (-b - np.sqrt(discriminant)) / (2 * a)
        # if t1 < 1e-8 and t2 < 1e-8:
        #     return None, None
        # if t1 < 1e-8:
        #     return t2, self
        # if t2 < 1e-8:
        #     return t1, self
        # return min(t1, t2), self

        # Vector from the ray origin to the sphere center
        L = ray.origin - self.center

        # Coefficients of the quadratic equation
        a = np.dot(ray.direction, ray.direction)
        b = 2 * np.dot(ray.direction, L)
        c = np.dot(L, L) - (self.radius ** 2)

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            return None, None  # No intersection
        # Calculate potential solutions
        sqrt_D = np.sqrt(discriminant)
        t1 = (-b + sqrt_D) / (2 * a)
        t2 = (-b - sqrt_D) / (2 * a)
        if t1 < epsilon and t2 < epsilon:
            return None, None
        if t1 < epsilon:
            return t2, self
        if t2 < epsilon:
            return t1, self
        return min(t1, t2), self
