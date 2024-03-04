This jar is built from source from [google/jarjar](git@github.com:google/jarjar.git)
from commit 17b3a0484826f6873c5a971faec89bee8574af80, built on March 1, 2024
using java version : 17.0.8 2023-07-18 LTS


To build from source, follow these instructions:

1. Clone the repository into a local folder.
2. Copy the latest ant jar available in the [gwt tools](https://github.com/gwtproject/tools/tree/main/lib/apache)
repository into the `lib` folder of the cloned repo.
3. Run `ant dist` in the root folder of the repository.
4. Find the jar `jarjar-1.4.jar` in the `dist` folder.