import numpy as np


# This function gets a vector and returns its normalized form.
def normalize(vector):
    return (vector / np.linalg.norm(vector))


# This function gets a vector and the normal of the surface it hit
# This function returns the vector that reflects from the surface
def reflected(vector, axis):
    dot_product = np.dot(vector, axis)
    return vector - 2 * dot_product * axis


## Lights


class LightSource:
    def __init__(self, intensity):
        self.intensity = intensity


class DirectionalLight(LightSource):

    def __init__(self, intensity, direction):
        super().__init__(intensity)
        self.direction = direction

    # This function returns the ray that goes from the light source to a point
    def get_light_ray(self, intersection_point):
        return Ray(intersection_point, normalize(-self.direction))

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
        self.direction = normalize(np.array(direction))
        self.kc = kc
        self.kl = kl
        self.kq = kq

    # This function returns the ray that goes from a point to the light source
    def get_light_ray(self, intersection):
        return Ray(intersection, normalize(-self.direction))

    def get_distance_from_light(self, intersection):
        return np.linalg.norm(intersection - self.position)

    def get_intensity(self, intersection):
        distance_from_light = self.get_distance_from_light(intersection)
        direction_to_point = normalize(intersection - self.position)
        dot_product = np.dot(direction_to_point, self.direction)
        return self.intensity * dot_product / (
                    self.kc + self.kl * distance_from_light + self.kq * (distance_from_light ** 2))

        # direction_to_point = normalize(intersection - self.position)
        # dot_product = np.dot(direction_to_point, self.direction)
        # if dot_product < 0:  # Light does not reach the point if the angle is obtuse
        #     return 0
        # d = self.get_distance_from_light(intersection)
        # intensity_at_intersection = self.intensity * dot_product / (self.kc + self.kl * d + self.kq * d ** 2)
        # return intensity_at_intersection


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    # The function is getting the collection of objects in the scene and looks for the one with minimum distance.
    # The function should return the nearest object and its distance (in two different arguments)
    def nearest_intersected_object(self, objects):
        nearest_object = None
        min_distance = np.inf
        intersection_point = None
        for obj in objects:
            t, _ = obj.intersect(self)
            if t is not None:
                distance = np.linalg.norm(self.origin + t * self.direction - self.origin)
                if distance < min_distance:
                    min_distance = distance
                    nearest_object = obj
                    intersection_point = self.origin + t * self.direction
        return nearest_object, min_distance, intersection_point


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
        self.normal = normalize(np.array(normal))
        self.point = np.array(point)

    def intersect(self, ray: Ray):
        epsilon = 1e-6
        v = self.point - ray.origin
        t = np.dot(v, self.normal) / (np.dot(self.normal, ray.direction) + epsilon)
        if t > 0:
            return t, self
        else:
            return None, None


class Triangle(Object3D):
    """
        C
        /\
       /  \
    A /____\ B

    The fornt face of the triangle is A -> B -> C.

    """

    def __init__(self, a, b, c):
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)
        self.normal = self.compute_normal()

    # computes normal to the trainagle surface. Pay attention to its direction!
    def compute_normal(self):
        ab = self.b - self.a
        ac = self.c - self.a
        return normalize(np.cross(ab, ac))

    def intersect(self, ray):
        ab = self.b - self.a
        ac = self.c - self.a
        A = np.column_stack((ab, ac, -ray.direction))
        b = ray.origin - self.a
        try:
            # Solving the system using numpy's linear algebra solver
            u, v, t = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # This occurs if the matrix A is singular, i.e., no solution
            return np.inf, None

        # Check if the solution is within the bounds of the triangle and ray is pointing towards it
        if u >= 0 and v >= 0 and (u + v) <= 1 and t >= 0:
            return t, self
        else:
            return np.inf, None


class Pyramid(Object3D):
    """
            D
            /\*\
           /==\**\
         /======\***\
       /==========\***\
     /==============\****\
   /==================\*****\
A /&&&&&&&&&&&&&&&&&&&&\ B &&&/ C
   \==================/****/
     \==============/****/
       \==========/****/
         \======/***/
           \==/**/
            \/*/
             E

    Similar to Traingle, every from face of the diamond's faces are:
        A -> B -> D
        B -> C -> D
        A -> C -> B
        E -> B -> A
        E -> C -> B
        C -> E -> A
    """

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
            [2, 4, 0]]
        for idx in t_idx:
            # Assume Triangle takes three vertices as its parameters
            l.append(Triangle(self.v_list[idx[0]], self.v_list[idx[1]], self.v_list[idx[2]]))
        return l

    def apply_materials_to_triangles(self):
        for triangle in self.triangle_list:
            triangle.set_material(self.material["ambient"], self.material["diffuse"], self.material["specular"],
                                  self.material["shininess"], self.material["reflection"])

    def intersect(self, ray: Ray):
        min_distance = np.inf  # Store the closest intersection distance
        closest_triangle = None
        min_t = np.inf

        for triangle in self.triangle_list:
            intersection = triangle.intersect(ray)  # Assuming intersect method returns (distance, point) or None
            if intersection is not None:
                t, obj = intersection
                distance = np.linalg.norm(ray.origin + t * ray.direction - ray.origin)
                # Update if this is the first intersection or closer than the previous one
                if distance < min_distance:
                    min_distance = distance
                    min_t = t
                    closest_triangle = obj

        # Return the closest intersection point and distance, if any
        if closest_triangle is None:
            return np.inf, None
        return min_t, closest_triangle


class Sphere(Object3D):
    def __init__(self, center, radius: float):
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray):
        # Vector from the ray origin to the sphere center
        L = ray.origin - self.center

        # Coefficients of the quadratic equation
        A = np.dot(ray.direction, ray.direction)
        B = 2 * np.dot(ray.direction, L)
        C = np.dot(L, L) - (self.radius ** 2)

        # Discriminant
        D = B ** 2 - 4 * A * C

        if D < 0:
            return np.inf, None  # No intersection
        else:
            # Calculate potential solutions
            sqrt_D = np.sqrt(D)
            t1 = (-B + sqrt_D) / (2 * A)
            t2 = (-B - sqrt_D) / (2 * A)

            # Filter out negative values, as they represent intersections behind the ray's origin
            t = np.array([t for t in [t1, t2] if t >= 0])
            if t.size == 0:
                return np.inf, None  # No positive t, meaning all intersections are behind the origin

            # Find the closest intersection
            t_closest = np.min(t)

            return t_closest, self
