import numpy as np


# This function gets a vector and returns its normalized form.
def normalize(vector):
    return vector / np.linalg.norm(vector)


# This function gets a vector and the normal of the surface it hit
# This function returns the vector that reflects from the surface
def reflected(vector, axis):
    # TODO:
    v = np.array([0,0,0])
    dot_product = np.dot(vector, axis)
    v = vector - 2 * dot_product * axis
    return v

## Lights


class LightSource:
    def __init__(self, intensity):
        self.intensity = intensity


class DirectionalLight(LightSource):

    def __init__(self, intensity, direction):
        super().__init__(intensity)
        # TODO
        self.direction = normalize(np.array(direction)) 

    # This function returns the ray that goes from the light source to a point
    def get_light_ray(self,intersection_point):
        # TODO
        return Ray(intersection_point,-self.direction)

    # This function returns the distance from a point to the light source
    def get_distance_from_light(self, intersection):
        #TODO
        return np.inf

    # This function returns the light intensity at a point
    def get_intensity(self, intersection):
        #TODO
        return self.intensity


class PointLight(LightSource):
    def __init__(self, intensity, position, kc, kl, kq):
        super().__init__(intensity)
        self.position = np.array(position)
        self.kc = kc
        self.kl = kl
        self.kq = kq

    # This function returns the ray that goes from a point to the light source
    def get_light_ray(self,intersection):
        return Ray(intersection, normalize(self.position - intersection))

    # This function returns the distance from a point to the light source
    def get_distance_from_light(self,intersection):
        return np.linalg.norm(intersection - self.position)

    # This function returns the light intensity at a point
    def get_intensity(self, intersection):
        d = self.get_distance_from_light(intersection)
        return self.intensity / (self.kc + self.kl*d + self.kq * (d**2))
    


class SpotLight(LightSource):
    def __init__(self, intensity, position, direction, kc, kl, kq):
        super().__init__(intensity)
        # TODO
        self.position = np.array(position)
        self.direction = normalize(np.array(direction))  
        self.kc = kc
        self.kl = kl
        self.kq = kq

    # This function returns the ray that goes from the light source to a point
    def get_light_ray(self, intersection):
        #TODO
        direction_to_point = normalize(intersection - self.position)
        return Ray(self.position, direction_to_point)

    def get_distance_from_light(self, intersection):
        #TODO
        return np.linalg.norm(intersection - self.position)

    def get_intensity(self, intersection):
        #TODO
        direction_to_point = normalize(intersection - self.position)
        dot_product = np.dot(direction_to_point, -self.direction)
        if dot_product < 0:  # Light does not reach the point if the angle is obtuse
            return 0
        d = self.get_distance_from_light(intersection)
        intensity_at_intersection = self.intensity * dot_product / (self.kc + self.kl * d + self.kq * d**2)
        return intensity_at_intersection


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    # The function is getting the collection of objects in the scene and looks for the one with minimum distance.
    # The function should return the nearest object and its distance (in two different arguments)
    def nearest_intersected_object(self, objects):
        intersections = None
        nearest_object = None
        min_distance = np.inf
        #TODO
        for obj in objects:
            distance = obj.intersect(self)
            if distance is not None and distance < min_distance:
                min_distance = distance
                nearest_object = obj
        return nearest_object, min_distance


class Object3D:
    def set_material(self, ambient, diffuse, specular, shininess, reflection):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection


class Plane(Object3D):
    def __init__(self, normal, point):
        self.normal = np.array(normal)
        self.point = np.array(point)

    def intersect(self, ray: Ray):
        v = self.point - ray.origin
        t = np.dot(v, self.normal) / (np.dot(self.normal, ray.direction) + 1e-6)
        if t > 0:
            return t, self
        else:
            return None


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
        # TODO
        ab = self.b - self.a
        ac = self.c - self.a
        return np.cross(ab, ac)

    def intersect(self, ray):
            A = np.column_stack((self.a - self.b, self.a - self.c, -ray.direction))
            b = ray.origin - self.a 
            try:
                # Solving the system using numpy's linear algebra solver
                u, v, t = np.linalg.solve(A, b)
            except np.linalg.LinAlgError:
                # This occurs if the matrix A is singular, i.e., no solution
                return None

            # Check if the solution is within the bounds of the triangle and ray is pointing towards it
            if u >= 0 and v >= 0 and (u + v) <= 1 and t >= 0:
                intersection_point = ray.origin + t * ray.direction
                return (intersection_point, t)
            else:
                return None

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
                [0,1,3],
                [1,2,3],
                [0,3,2],
                 [4,1,0],
                 [4,2,1],
                 [2,4,0]]
        # TODO
        return l

    def apply_materials_to_triangles(self):
        # TODO
        pass

    def intersect(self, ray: Ray):
        # TODO
        pass

class Sphere(Object3D):
    def __init__(self, center, radius: float):
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray):
        #TODO
        pass

