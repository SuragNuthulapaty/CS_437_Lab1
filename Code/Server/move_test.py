import move

m = move.Move()

while True:
    d = input()
    amt = input

    if d == 'f':
        m.forward()
    elif d == 'b':
        m.back()
    elif d == 'r':
        m.right(int(amt))
    elif d == 'l':
        m.left(int(amt))
