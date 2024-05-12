from helper_classes import *
import matplotlib.pyplot as plt


def get_color(scene, ray, depth, max_depth):
    if depth > max_depth:
        return np.zeros(3)

    epsilon = 1e-6
    color = np.zeros(3)
    nearest_object, min_distance, intersection_point = ray.nearest_intersected_object(scene['objects'])

    if nearest_object is None:
        return color

    normal = np.zeros(3)
    if isinstance(nearest_object, Plane) or isinstance(nearest_object, Triangle):
        normal = nearest_object.normal
    elif isinstance(nearest_object, Sphere):
        normal = normalize(intersection_point - nearest_object.center)

    color += add_ambient_light(scene['ambient'], nearest_object.material['ambient'], color)

    for light in scene['lights']:
        color = add_diffuse_light(normal, nearest_object.material['diffuse'], light, color, intersection_point)
        color = add_specular_light(normal, nearest_object.material['specular'], nearest_object.material['shininess'],
                                   light, color, intersection_point)

    if depth < max_depth:
        reflection_direction = reflected(-ray.direction, normal)
        reflection_ray = Ray(intersection_point, reflection_direction)
        reflection_color = get_color(scene, reflection_ray, depth + 1, max_depth)
        color += nearest_object.material['reflection'] * reflection_color

    return color


def add_ambient_light(scene_ambient, material_ambient, color):
    color += scene_ambient * material_ambient
    return color


def add_diffuse_light(normal, material_diffuse, light, color, intersection_point):
    light_ray = light.get_light_ray(intersection_point)
    light_intensity = light.get_intensity(intersection_point)
    diffuse_intensity = np.dot(normal, light_ray.direction)
    color += light_intensity * diffuse_intensity * material_diffuse
    return color


def add_specular_light(normal, material_specular, material_shininess, light, color, intersection_point):
    light_ray = light.get_light_ray(intersection_point)
    reflected_light = normalize(reflected(-light_ray.direction, normal))
    light_intensity = light.get_intensity(intersection_point)
    specular_intensity = np.dot(-light_ray.direction, reflected_light) ** material_shininess
    color += light_intensity * specular_intensity * material_specular
    return color


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

            nearest_object, _, _ = ray.nearest_intersected_object(objects)
            if nearest_object is None:
                color = np.zeros(3)
            else:
                color = get_color(scene, ray, 0, max_depth)

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
