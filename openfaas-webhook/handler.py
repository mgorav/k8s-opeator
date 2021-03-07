import json

from flask import jsonify, make_response


def handle(req):
    print('MetaController-FAAS')
    req_json = json.loads(req)
    parent = req_json['parent']
    children = req_json['children']
    # Compute status based on observed state.
    desired_status = {
        "pods": len(children["Pod.v1"])
    }

    print("len(children[Pod.v1] = " + str(len(children["Pod.v1"])))
    print("parent[metadata][name] = " + parent["metadata"]["name"])

    # Generate the desired child object(s).
    who = parent.get("spec", {}).get("who", "World")
    print("who = " + who)
    desired_pods = [
        {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": parent["metadata"]["name"]
            },
            "spec": {
                "restartPolicy": "OnFailure",
                "containers": [
                    {
                        "name": "hello",
                        "image": "busybox",
                        "command": ["echo", "Hello, %s!" % who]
                    }
                ]
            }
        }
    ]

    output = {"status": desired_status, "children": desired_pods}

    print(output)

    return make_response(jsonify(output), 200, {'Content-Type': 'application/json'})
