# Large Image Handling for Trame

*Large image viewer for Trame*

Trame widgets to serve tiles and visualize large images
(geospatial or otherwise). This package uses Kitware's
[large-image](https://github.com/girder/large_image)
for image handling.

The dynamic tile server provided here prevents the need for preprocessing large images into tile sets for viewing interactively on slippy-maps. Under the hood, large-image applies operations (rescaling, reprojection, image encoding) to create image tiles on-the-fly.

* Free software: Apache Software License

| Geospatial | Medical |
|---|---|
| ![geo](./assets/new-york.png) | ![med](./assets/kidney.png) |


# Installing from Source

Build and install the Vue components

```bash
cd vue-components
npm i
npm run build
cd -
```

Install the application

```bash
pip install -e .
```


# Examples

See demos in the `examples/` directory and related data in the `data/` directory.
