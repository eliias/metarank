from datetime import datetime 

from metarank import Client
from metarank.schemas import FeedbackSchema, IdSchema, FieldSchema

event_counter = 1


def event_id() -> str:
    global event_counter
    new_event_id = f"event:{event_counter}"
    event_counter += 1
    return new_event_id


def run():
    base_url = "http://localhost:8080"
    
    client = Client(base_url)
    is_healthy = client.health_check()
    print(f"Is metarank healthy?: {is_healthy}")
    
    metrics = client.metrics()
    print(f"Metrics: {metrics}")
    
    now = datetime.now().astimezone().isoformat()
    
    events = [
        FeedbackSchema(
            event="item",
            id=event_id(),
            timestamp=now,
            item="item:1",
            fields=[
                FieldSchema(
                    name="color",
                    value="red"
                )
            ]
        ),
        FeedbackSchema(
            event="item",
            id=event_id(),
            timestamp=now,
            item="item:3",
            fields=[
                FieldSchema(
                    name="color",
                    value="red"
                )
            ]
        ),
        FeedbackSchema(
            event="item",
            id=event_id(),
            timestamp=now,
            item="item:3",
            fields=[
                FieldSchema(
                    name="color",
                    value="blue"
                )
            ]
        ),
        FeedbackSchema(
            event="ranking",
            id=event_id(),
            items=[
                IdSchema(id="item:3"),
                IdSchema(id="item:1"),
                IdSchema(id="item:2"),
            ],
            user="hannes",
            session="session:1",
            timestamp=now
        ),
        FeedbackSchema(
            event="ranking",
            id=event_id(),
            items=[
                IdSchema(id="1")
            ],
            user="neele",
            session="session:2",
            timestamp=now
        )
    ]
    
    for feedback_data in events:
        response = client.feedback(feedback_data=feedback_data)
        print(response)
 

if __name__ == '__main__':
    run()
