# Math
* All methods that doesn't use randomization or related to sketch content is removed from the `Sketch` class.
* Replaces `py5.mixins.math.MathMixin.random_seed` with property based approach.
  * New: `pier5.random.RandomMixin.seed` returns the current seed
  * Replacement: Setting `pier5.random.RandomMixin.seed` updates the seed and rng.
* Renames `Sketch._rng` to `.rng
* Removes redefinition of trigonometric functions from `pier5.math`, proxies np imports.
* Removed `dist()`, introduces `dist_2d()` and `dist_3d()`
  * Introduces `Point2D` and `Point3D` classes as input arg types, respectively.
* `Sketch` methods accept only keyword arguments.
* Trigonometric functions are removed from the library context. Alternatives are:
  * sin: Use `numpy.sin()`
  * asin: Use `numpy.arcsin()`
  * cos: Use `numpy.cos()`
  * acos: Use `numpy.arccos()`
  * tan: Use `numpy.tan()`
  * atan: Use `numpy.arctan()`
  * tan2: Use `numpy.tan2()`
  * atan2: Use `numpy.arctan2()`
*
