from helper_classes import *
import matplotlib.pyplot as plt


def get_color(scene, ray, depth, max_depth):
    if depth > max_depth:
        return np.zeros(3)

    nearest_object, min_t, intersection_point = ray.nearest_intersected_object(scene["objects"])
    if nearest_object is None:
        return np.zeros(3)

    color = np.zeros(3)

    # Ambient light
    color += get_ambient_light(scene["ambient"], nearest_object.material)

    normal = np.zeros(3)
    if isinstance(nearest_object, Plane) or isinstance(nearest_object, Triangle):
        normal = nearest_object.normal
    elif isinstance(nearest_object, Sphere):
        normal = normalize(intersection_point - nearest_object.center)

    for light in scene["lights"]:
        if is_in_shadow(scene["objects"], light, intersection_point):
            color += get_diffuse_light(light, nearest_object.material, normal, intersection_point)
            color += get_specular_light(light, nearest_object.material, normal, intersection_point, ray)

    if depth + 1 > max_depth:
        return color

    reflected_ray = Ray(intersection_point, normalize(reflected(ray.direction, normal)))
    reflected_color = get_color(scene, reflected_ray, depth + 1, max_depth)
    color += nearest_object.material['reflection'] * reflected_color

    return color


def get_ambient_light(ambient, material):
    return ambient * material['ambient']


def is_in_shadow(objects, light, intersection_point):
    if isinstance(light, DirectionalLight):
        direction_to_light = normalize(light.direction)
    else:
        direction_to_light = normalize(light.position - intersection_point)
    biased_intersection = intersection_point + direction_to_light * epsilon
    shadow_ray = Ray(biased_intersection, direction_to_light)
    shadow_distance = light.get_distance_from_light(intersection_point)
    nearest_object, min_t, _ = shadow_ray.nearest_intersected_object(objects)
    if nearest_object is not None and min_t < shadow_distance:
        return False
    return True


def get_diffuse_light(light, material, normal, intersection_point):
    direction_to_light = normalize(light.get_light_ray(intersection_point).direction)
    light_intensity = light.get_intensity(intersection_point)
    diffuse = np.dot(direction_to_light, normal)
    return material['diffuse'] * light_intensity * max(diffuse, 0)


def get_specular_light(light, material, normal, intersection_point, ray):
    direction_to_light = normalize(light.get_light_ray(intersection_point).direction)
    direction_to_camera = normalize(ray.origin - intersection_point)
    direction_reflected = reflected(direction_to_light, normal)
    specular = np.dot(direction_reflected, direction_to_camera)
    light_intensity = light.get_intensity(intersection_point)
    return material['specular'] * light_intensity * max(specular, 0) ** material['shininess']


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
                color = get_color(scene, ray, 1, max_depth)

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
