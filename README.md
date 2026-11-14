# food-picture-01: Rendang, Dark and Glossy

Entry for make.fun's food-picture-01: the best-looking food picture.

The program copies the bundled photograph of Indonesian beef rendang
-- dark caramelised beef chunks glistening in thick coconut curry
sauce, served with steamed white rice -- to the output directory as
`entry.png`.

## Run

```sh
python3 main.py
```

It writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`, or to `/output` when
that variable is not set. The image is a real PNG, 832x832 pixels,
under the competition's 1 MiB cap, so the program only copies bytes
after checking the size, the PNG magic, the dimensions and the
trailing IEND chunk.
