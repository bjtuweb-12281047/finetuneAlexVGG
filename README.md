# Finetune AlexNet & VGG with Tensorflow

My AlexNet and VGG16 model implementations for Tensorflow, with a validation and finetune/retrain script.
Also includes wrapper model classes to use the Tensorflow Slim implementations of VGG16 and Inception V3 (finetune does not really work with those so far).
Comes with Jupyter notebooks to test the different preprocessing scripts, run a classification and finetune a model using a notebook.

## Requirements

- Python 2.7 or 3
- TensorFlow >= 1.13rc0 (I guess everything from version 1.0 on will work)
- Numpy

## Content

- `validate.py`: Script to validate the implemented models and the downloaded weights 
- `finetune.py`: Script to run the finetuning process
- `helper/*`: Contains helper scripts/classes to load data and run the retraining
- `models/*`: Contains a parent model class and different model implementations (AlexNet, VGG, Inception)
- `images/*`: contains 4 example images, used in the validation script
- `preprocessing/*`: Contains scripts to run different ways of image preprocessing (crop, resize, ...).

# Weights:
- AlexNet: http://www.cs.toronto.edu/%7Eguerzhoy/tf_alexnet/bvlc_alexnet.npy
- VGG16: https://mega.nz/a96db891-9e0d-1644-bee9-b2679aa26378
- Inception V3 (checkpoint): http://download.tensorflow.org/models/inception_v3_2016_08_28.tar.gz
- VGG16 (Slim impl. / checkpoint): http://download.tensorflow.org/models/vgg_16_2016_08_28.tar.gz

## Usage

### Validate the model implementations, image preprocessing and initial weights
```
python validate.py -model alex
...
python validate.py -model [alex, vgg, vgg_slim, inc_v3]
```



### Run finetuning/retraining on selected layers
```
python finetune.py -image_path /path/to/images -model alex
...
python finetune.py -image_path /path/to/images -model [alex, vgg]
python finetune.py -image_file /path/to/images.txt -model [alex, vgg]
```

Using: `-image_dir`: `/path/to/images` should point to a folder with a set of sub-folders, each named after one of your final categories and containing only images from that category.
Using: `-image_file`: `/path/to/images.txt` should be a file with a list of image-paths and labels. 

e.g.
```
cat /path/to/cat1.jpg
cat /path/to/cat2.jpg
dog /path/to/dog1.jpg
...
```

Other option:
- `-write_checkpoint_on_each_epoch`: Save a checkpint on each epoch (default is just at the end)
```
python finetune.py ... -write_checkpoint_on_each_epoch
```
- `-init_from_ckpt /path/to/file.ckpt`: Start the training from a saved checkpoint file by providing the path to that file (will restore weights on all layers).
Usually the initial weights are the pretrained imagenet weights (numpy-file or checkpoint), without restoring the retrain layers.
```
python finetune.py ... -init_from_ckpt /path/to/file.ckpt
```
- `-use_adam_optimizer`: Set this to use the AdamOptimizer for training. By default the GradientDescentOptimizer will be used.
```
python finetune.py ... -use_adam_optimizer
```

### Create Features
You can create features (activations at a given layer) and save them to the filesystem.
The featues will be stored as `.txt` files. The filename is the MD5 hash for the filepath.
In addidion a mapping file will be created.

The `-image_path`/`-image_file` and `-model` parameter work the same way as they do for finetuning.
In addition you need to provide the layer you want to use by adding `-layer` (e.g. `-layer fc6`) and 
the location the features should be stored with `-feature_dir` (e.g. `-feature_dir /path/to/features`)
```
python create_features.py -image_path /path/to/images -model vgg -layer fc6 -feature_dir /path/to/features
python create_features.py -image_file /path/to/images.txt -model inc_v3 -layer PreLogits -feature_dir /path/to/features
...
python create_features.py -image_path /path/to/images -model [alex, vgg, inc_v3] -layer layername -feature_dir /path/to/features
```

# Useful sources:
- https://kratzert.github.io/2017/02/24/finetuning-alexnet-with-tensorflow.html
- https://kratzert.github.io/2017/06/15/example-of-tensorflows-new-input-pipeline.html
- https://www.cs.toronto.edu/~frossard/post/vgg16/
- https://github.com/machrisaa/tensorflow-vgg
