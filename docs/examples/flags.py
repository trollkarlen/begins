import begin


@begin.start
def question(enabled=False, disabled=True):
    print("enable:", enabled)
    print("disable:", disabled)
