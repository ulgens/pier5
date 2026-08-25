from pier5 import BaseSketch

s = BaseSketch()
print(s.seed)
print(s.rng)

print(s.random_int())


print(s.random_int(low=4, high=80))
