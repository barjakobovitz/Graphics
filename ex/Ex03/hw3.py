from helper_classes import *
import matplotlib.pyplot as plt


<<<<<<< HEAD
=======
def get_color(scene, ray, depth, max_depth):
    if depth > max_depth:
        return np.zeros(3)

    epsilon = np.finfo(float).eps
    color = np.zeros(3)
    nearest_object, min_distance = ray.nearest_intersected_object(scene['objects'])
    if nearest_object is None:
        return color

    intersection = ray.origin + min_distance * ray.direction
    normal = np.zeros(3)
    if isinstance(nearest_object, Plane) or isinstance(nearest_object, Triangle):
        normal = nearest_object.normal
    elif isinstance(nearest_object, Sphere):
        normal = normalize(intersection - nearest_object.center)

    color += nearest_object.material['ambient'] * scene['ambient']

    for light in scene['lights']:
        light_ray = light.get_light_ray(intersection)
        light_intensity = light.get_intensity(intersection)

        shadow_ray = Ray(intersection + epsilon * normal, light_ray.direction)
        shadow_object, shadow_distance = shadow_ray.nearest_intersected_object(scene['objects'])
        if shadow_object is None or shadow_object == nearest_object:
            L = normalize(light_ray.direction)
            diffuse = max(np.dot(normal, L), 0)
            color += light_intensity * diffuse * nearest_object.material['diffuse']

            V = normalize(ray.origin - intersection)
            R = reflected(-L, normal)
            specular = np.power(max(np.dot(R, V), 0), nearest_object.material['shininess'])
            color += light_intensity * specular * nearest_object.material['specular']

    if depth <= max_depth and nearest_object.material['reflection'] > 0:
        reflection_direction = reflected(ray.direction, normal)
        reflection_ray = Ray(intersection + epsilon * normal, reflection_direction)
        reflection_color = get_color(scene, reflection_ray, depth + 1, max_depth)
        color += nearest_object.material['reflection'] * reflection_color

    return color


>>>>>>> 8e20eae58523a578b5a9247e6fecf5efbd817a43
def render_scene(camera, ambient, lights, objects, screen_size, max_depth):
    width, height = screen_size
    ratio = float(width) / height
    screen = (-1, 1 / ratio, 1, -1 / ratio)  # left, top, right, bottom

    image = np.zeros((height, width, 3))

    for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
        for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
            # screen is on origin
            pixel = np.array([x, y, 0])
            origin = camera
            direction = normalize(pixel - origin)
            ray = Ray(origin, direction)

            color = np.zeros(3)
<<<<<<< HEAD

            # This is the main loop where each pixel color is computed.
            # TODO
            color = recursive_color(ray, 0, max_depth, objects, lights, camera, ambient)
=======
            nearest_object, min_distance = ray.nearest_intersected_object(objects)
            if nearest_object is None:
                color = np.zeros(3)
            else:
                scene = {"objects": objects, "ambient": ambient, "lights": lights}
                color = get_color(scene, ray, 0, max_depth)

>>>>>>> 8e20eae58523a578b5a9247e6fecf5efbd817a43
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
