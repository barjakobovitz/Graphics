from helper_classes import *
import matplotlib.pyplot as plt


def get_color(scene, ray, depth, max_depth):
    color = np.zeros(3)
    is_in_shadow = True
    nearest_object, min_t, intersection_point = ray.nearest_intersected_object(scene["objects"])

    if nearest_object is None:
        return color

    normal = np.zeros(3)
    if nearest_object.__class__.__name__ == "Plane" or nearest_object.__class__.__name__ == "Triangle":
        normal = nearest_object.normal
    elif nearest_object.__class__.__name__ == "Sphere":
        normal = normalize(intersection_point - nearest_object.center)

    for light in scene["lights"]:
        is_in_shadow = get_is_in_shadow(scene["objects"], light, intersection_point)
        color += get_diffuse_light(light, nearest_object.material, normal, intersection_point) * (1 - is_in_shadow)
        color += get_specular_light(light, nearest_object.material, normal, intersection_point, ray) * (
                    1 - is_in_shadow)

    if not is_in_shadow:
        color += get_ambient_light(scene["ambient"], nearest_object.material)

    if depth + 1 > max_depth:
        return color

    reflected_ray = Ray(intersection_point, normalize(reflected(ray.direction, normal)))
    reflected_color = get_color(scene, reflected_ray, depth + 1, max_depth)
    color += nearest_object.material['reflection'] * reflected_color

    return color


def get_ambient_light(ambient, material):
    return ambient * material['ambient']


def get_is_in_shadow(objects, light, intersection_point):
    light_ray = light.get_light_ray(intersection_point)
    light_distance = light.get_distance_from_light(intersection_point)
    nearest_object, _, nearest_object_intersection_point = light_ray.nearest_intersected_object(objects)
    if nearest_object is None:
        return False
    else:
        nearest_object_distance = np.linalg.norm(intersection_point - nearest_object_intersection_point)
        return nearest_object_distance < light_distance


def get_diffuse_light(light, material, normal, intersection_point):
    light_direction = light.get_light_ray(intersection_point).direction
    return material['diffuse'] * light.get_intensity(intersection_point) * np.dot(light_direction, normal)


def get_specular_light(light, material, normal, intersection_point, ray):
    light_direction = light.get_light_ray(intersection_point).direction
    reflection = normalize(reflected(-light_direction, normal))
    view_direction = -ray.direction
    return (material['specular'] * light.get_intensity(intersection_point) * np.dot(reflection, view_direction) **
            material['shininess'])


def render_scene(camera, ambient, lights, objects, screen_size, max_depth):
    width, height = screen_size
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

    image = np.zeros((height, width, 3))
    scene = {"objects": objects, "ambient": ambient, "lights": lights}

    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            # screen is on origin
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)
            ray = Ray(origin, direction)

            color = np.zeros(3)
            closest_object, min_t, intersection_point = ray.nearest_intersected_object(objects)
            if closest_object is not None:
                color += get_color(scene, ray, 1, max_depth)

            # We clip the values between 0 and 1 so all pixel values will make sense.
            image[i, j] = np.clip(color, 0, 1)

    return image


# Write your own objects and lights
# TODO
def your_own_scene():
    camera = np.array([0, 0, 1])
    lights = []
    objects = []
    return camera, lights, objects
