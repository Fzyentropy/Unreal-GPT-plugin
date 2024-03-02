import json
import openai
import unreal
import subprocess
import sys
import tempfile
import os
from openai import OpenAI

# Set your OpenAI API key
client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])

# Define the prompt components

system_prompt="You are an Unreal Engine 5 developer assistant.  You will respond to all request by writing an unreal engine 5 editor python script based on the user request.  Only respond with the python code and to not explain anything.  Here are a couple of valid responses.\n\nall_actors = unreal.EditorLevelLibrary.get_all_level_actors()\n\nfor actor in all_actors:\n    if isinstance(actor, unreal.StaticMeshActor) and actor.get_actor_label().startswith(\"Cube\"):\n       unreal.EditorLevelLibrary.destroy_actor(actor)\n        break\n\nunreal.log(\"Cube destroyed.\")\n\nimport math\n\nradius = 100\nspacing = 10\nnum_lights = int(math.ceil(radius/spacing))\n\nfor i in range(num_lights):\n    angle = i * math.pi * 2 / num_lights\n    x = math.cos(angle) * radius\n    y = math.sin(angle) * radius\n    location = unreal.Vector(x, y, 0)\n    unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight, location, unreal.Rotator(0, 0, 0))\n    \nunreal.log(\"Point lights spawned in a radius of 100 spaced 10 apart.\")\n\nLogPython: all_actors = unreal.EditorLevelLibrary.get_all_level_actors()\nfor actor in all_actors:\n    if isinstance(actor, unreal.PointLight):\n        location = actor.get_actor_location()\n        actor.set_actor_location(unreal.Vector(location.x, location.y, location.z+50), False, False)\n        \nunreal.log(\"Point lights moved up by 50.\")\n\nimport random\nimport unreal\nall_actors = unreal.EditorLevelLibrary.get_all_level_actors()\nfor actor in all_actors:\n    if isinstance(actor, unreal.PointLight):\n        new_color = unreal.LinearColor(random.random(), random.random(), random.random(), 1)\n        actor.set_light_color(new_color)\n\nunreal.log(\"lights set to random colors.\")\n\nall_actors = unreal.EditorLevelLibrary.get_all_level_actors()\npoint_lights = []\nfor actor in all_actors:\n    if isinstance(actor, unreal.PointLight):\n        point_lights.append(actor)\n        \nfor i in range(len(point_lights)):\n    for j in range(i+1, len(point_lights)):\n        loc_i = point_lights[i].get_actor_location()\n        loc_j = point_lights[j].get_actor_location()\n        direction = loc_i - loc_j\n        distance = direction.length()\n        new_distance = distance + 50\n        unit_direction = direction / distance\n        new_location_i = loc_i + (unit_direction * ((new_distance - distance) / 2))\n        new_location_j = loc_j - (unit_direction * ((new_distance - distance) / 2))\n        point_lights[i].set_actor_location(new_location_i, False, False)\n        point_lights[j].set_actor_location(new_location_j, False, False)\n\nimport unreal\ncube_static_mesh = unreal.EditorAssetLibrary.load_asset(\"/Engine/BasicShapes/Cube\")\nlocation = unreal.Vector(0, 0, 0)\nrotation = unreal.Rotator(0, 0, 0)\nactor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)\nstatic_mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent.static_class())\nstatic_mesh_component.set_static_mesh(cube_static_mesh)\n\nall_actors = unreal.EditorLevelLibrary.get_all_level_actors()\npoint_lights = []\n\nfor actor in all_actors:\n    if isinstance(actor, unreal.PointLight):\n        point_lights.append(actor)\n\ngroup_name = \"PointLightsGroup\"\ngroup_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.GroupActor, unreal.Vector(), unreal.Rotator())\ngroup_actor.set_actor_label(group_name)\n\nroot_component = group_actor.root_component\n\nfor actor in point_lights:\n    actor.attach_to_component(root_component, unreal.Name(\"\"), unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, False)\n\n"

user_prompt="Now help me create 10 cubes and 1 spotlight that spread randomly around (0,0,100)."


# Send the prompt to GPT-3.5 and retrieve the response

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
  ]
)


# Extract the JSON action from the response

response_text = completion.choices[0].message.content
response_text = response_text.replace('\\n', '\n')

print(response_text)

# Execute the GPT-3 response as Python code
exec(response_text)
#os.remove(temp_script.name)