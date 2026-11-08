import random



#get_task() test: verify tasks are being returne
def test_get_tasks(client, sample_task):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task(client, sample_task):
    task_id = sample_task["id"]


    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["task"] == "go to latina night"

def test_add_task(client, sample_task):
    response = client.post(url="/tasks",
                          json= {
                              "task": "go to latina night"
                            })
    new_task = response.json(client)
    task_added = client.get(f"/tasks/{new_task["id"]}").json()

    assert new_task == task_added

def test_update_task(client):
    current_tasks = client.get("/tasks").json()
    task_to_update = random.choice(current_tasks)

    updated_task = client.put(url=f"/tasks/{task_to_update["id"]}",json={"task": "drink a bev"}).json()

    assert updated_task["task"] == "drink a bev"

def test_finish_task(client):
    current_tasks = client.get("/tasks").json()
    task_to_finish = random.choice(current_tasks)

    finished_task = client.patch(f"/tasks/{task_to_finish["id"]}").json()

    assert finished_task["is_finished"]


def test_delete_task(client): 
    current_tasks = client.get("/tasks").json()
    task_to_delete = random.choice(current_tasks)

    response = client.delete(f"/tasks/{task_to_delete["id"]}")
    find_response = client.get(f"/tasks/{task_to_delete["id"]}")

    assert response.json()["message"] == "successfully deleted the task!"
    assert find_response.status_code == 404



    
