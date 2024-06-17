import numpy as np

from helper_classes import *
import matplotlib.pyplot as plt


def get_color(scene, ray, depth, max_depth):
    color = np.zeros(3)
    is_in_shadow = True
    nearest_object, min_t, intersection_point = ray.nearest_intersected_object(scene["objects"])

    if nearest_object is None:
        return color

    normal = np.zeros(3)
    if isinstance(nearest_object, Plane) or isinstance(nearest_object, Triangle):
        normal = nearest_object.normal
    elif isinstance(nearest_object, Sphere):
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
    camera = np.array([0, 0, 2])
    objects = []

    # Define stars with increased reflectivity and glow
    sirius = Sphere(np.array([-3, 2, -4]), 0.5)
    sirius.set_material(np.array([0.2, 0.2, 0.2]), np.array([1.0, 0.9, 0.8]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(sirius)

    canopus = Sphere(np.array([2, -1, -4]), 0.4)
    canopus.set_material(np.array([0.2, 0.2, 0.2]), np.array([0.9, 0.9, 0.7]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(canopus)

    alpha_centauri = Sphere(np.array([1, 3, -4]), 0.3)
    alpha_centauri.set_material(np.array([0.2, 0.2, 0.2]), np.array([0.9, 0.7, 0.5]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(alpha_centauri)

    arcturus = Sphere(np.array([-2, -3, -4]), 0.4)
    arcturus.set_material(np.array([0.2, 0.2, 0.2]), np.array([0.7, 0.5, 0.3]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(arcturus)

    vega = Sphere(np.array([3, 1, -4]), 0.3)
    vega.set_material(np.array([0.2, 0.2, 0.2]), np.array([0.8, 0.8, 1.0]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(vega)

    rigel = Sphere(np.array([-1, -2, -4]), 0.4)
    rigel.set_material(np.array([0.2, 0.2, 0.2]), np.array([1.0, 0.5, 0.5]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(rigel)

    sun = Sphere(np.array([0, 0, -4]), 0.3)
    sun.set_material(np.array([0.2, 0.2, 0.2]), np.array([1.0, 1.0, 0.9]), np.array([0.8, 0.8, 0.8]), 200, 0.5)
    objects.append(sun)

    # Define a spacecraft as a pyramid
    spacecraft = Pyramid(v_list=[
        np.array([1, 0, -3]),  # Tip
        np.array([0.8, -0.2, -3.2]),  # Base vertices
        np.array([1.2, -0.2, -3.2]),
        np.array([1.2, 0.2, -3.2]),
        np.array([0.8, 0.2, -3.2])
    ])
    spacecraft.set_material([0.8, 0.8, 0.8], [0.8, 0.8, 0.8], [0.5, 0.5, 0.5], 100, 0.5)
    spacecraft.apply_materials_to_triangles()
    objects.append(spacecraft)

    # Define the background as space
    background = Plane(normal=np.array([0, 0, 1]), point=np.array([0, 0, -5]))
    background.set_material([0, 0, 0], [0, 0, 0], [0, 0, 0], 1000, 0.1)
    objects.append(background)

    # Define a reflective plane (e.g., space station panel)
    plane = Plane(normal=np.array([0, 1, 0]), point=np.array([0, -1, -4]))
    plane.set_material([0.1, 0.1, 0.1], [0.6, 0.6, 0.6], [0.8, 0.8, 0.8], 500, 0.5)
    objects.append(plane)

    # Setup light sources
    directional_light = DirectionalLight(np.array([0.5, 0.5, 0.5]), np.array([1, 1, 1]))  # Simulating distant stars
    point_light = PointLight(np.array([1, 1, 1]), np.array([0, 0, 0]), 1, 0.1, 0.01)  # Simulating a bright star
    spot_light = SpotLight(np.array([0.5, 0.5, 0.5]), np.array([3, 3, 3]), np.array([1, -1, -1]), 1, 0.1, 0.01)  # Simulating a nebula
    lights = [directional_light, point_light, spot_light]

    return camera, lights, objects
