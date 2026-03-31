from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner()
    owner.name = "Alex"
    owner.email = "alex@example.com"

    dog = Pet()
    dog.name = "Buddy"
    dog.species = "Dog"
    dog.breed = "Golden Retriever"

    cat = Pet()
    cat.name = "Mittens"
    cat.species = "Cat"
    cat.breed = "Tabby"

    owner.add_pet(dog)
    owner.add_pet(cat)

    now = datetime.now()

    task1 = Task()
    task1.description = "Morning walk"
    task1.time = now + timedelta(hours=1)
    task1.frequency = "daily"

    task2 = Task()
    task2.description = "Feed breakfast"
    task2.time = now + timedelta(minutes=30)
    task2.frequency = "daily"

    task3 = Task()
    task3.description = "Evening play session"
    task3.time = now + timedelta(hours=5)
    task3.frequency = "daily"

    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    scheduler = Scheduler(owner)
    all_tasks = scheduler.organize_tasks(scheduler.retrieve_tasks())

    print("Today's Schedule")
    print("================")
    for t in all_tasks:
        status = "Done" if t.completion_status else "Pending"
        due = t.time.strftime("%Y-%m-%d %H:%M") if t.time else "No time set"
        print(f"{due} - {t.description} ({t.frequency}) [{status}]")


if __name__ == "__main__":
    main()
