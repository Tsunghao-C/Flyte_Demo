import flytekit as fl


image_spec = fl.ImageSpec(

    # The name of the image. This image will be used byt he say_hello task
    name="simple_cal",

    # Lock file with dependencies to install in image
    requirements="uv.lock",
)


@fl.task(container_image=image_spec)
def task_1(a: int, b: int, c: int) -> int:
    return a + b + c

@fl.task(container_image=image_spec)
def task_2(m: int, n: int) -> int:
    return m * n

@fl.task(container_image=image_spec)
def task_3(x: int, y: int) -> int:
    return x - y

@fl.workflow
def my_workflow(a: int = 3, b: int = 4, c: int = 5, m: int = 6, n: int = 7) -> int:
    x = task_1(a=a, b=b, c=c)
    y = task_2(m=m, n=n)
    return task_3(x=x, y=y)


if __name__ == "__main__":
    my_workflow(a=1, b=2, c=3, m=4, n=5)