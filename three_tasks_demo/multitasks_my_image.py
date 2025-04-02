import flytekit as fl


@fl.task(container_image="tsuchen/flyte-ml-demo")
def task_1(a: int, b: int, c: int) -> int:
    return a + b + c

@fl.task(container_image="tsuchen/flyte-ml-demo")
def task_2(m: int, n: int) -> int:
    return m * n

@fl.task(container_image="tsuchen/flyte-ml-demo")
def task_3(x: int, y: int) -> int:
    return x - y

@fl.task(container_image="tsuchen/flyte-ml-demo")
def task_4(x: int, y: int) -> int:
    return x + y

@fl.workflow
def my_workflow(a: int = 3, b: int = 4, c: int = 5, m: int = 6, n: int = 7) -> int:
    x = task_1(a=a, b=b, c=c)
    y = task_2(m=m, n=n)
    z = task_2(m=n, n=m)
    a = task_3(x=x, y=y)
    b = task_3(x=x, y=z)
    return task_4(x=a, y=b)


if __name__ == "__main__":
    my_workflow(a=1, b=2, c=3, m=4, n=5)