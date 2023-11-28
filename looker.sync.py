# %%
from pycocotools.coco import COCO
import os
import matplotlib.pyplot as plt
import numpy as np
import polars as pb
from PIL import Image
from finder.tools import group_anns, COCO_Image_Search, Record


# %%
# %load_ext autoreload
# %autoreload 2

# %%
# %aimport finder.tools

# %%
data_dir= './data'
data_type = 'train2017'
ann_file = f"{data_dir}/annotations/instances_train2017.json"
img_dir = './data/train2017'
caps_annFile = f'{data_dir}/annotations/captions_train2017.json'
print(os.getcwd())

# %%
coco = COCO(ann_file)
coco_caps = COCO(caps_annFile)

# %%
search_terms = ['person']
catIds = coco.getCatIds(catNms=search_terms)
imgIds = coco.getImgIds(catIds=catIds)
print(f"Found {len(imgIds)} entries matching search.")

# %%
capIds = coco_caps.getAnnIds(imgIds=imgIds)
caps = coco_caps.loadAnns(capIds)
imgs = coco.loadImgs(imgIds)
print(f"found {len(imgs)} images and {len(caps)} captions")

# %%
df = pb.DataFrame(caps)

# %%
search_results = df.filter(pb.col('caption').str.contains('big'))['image_id']
print(f"Found {len(search_results)} images")
path_gen = gen_search_groups(search_results)


# %%
test_paths = next(path_gen)
print(test_paths)

# %%
fig, axs = plt.subplots(4, 3, figsize=(15, 20))
img_paths = next(path_gen)
for x, ax in zip(img_paths, axs.flatten()):
    img = np.asarray(Image.open(x))
    print(x)
    ax.axis('off')
    ax.set_title(x)
    ax.imshow(img)
fig.tight_layout(pad=.75)
plt.show()


# %%
img_caps = group_anns(caps)
len(img_caps)

# %%
search_terms = ['person', 'horse', 'airplane']

# %%
img_search = COCO_Image_Search()


# %%
img_search.coco.cats

# %%
categories = []
r_pattern = ['vampire']
images = img_search.cat_search(categories).caption_contains(r_pattern).get_results()
print(len(img_search.img_ids))
print(images)

# %%
fig, axs = plt.subplots(4, 3, figsize=(15, 20))
img_paths = next(images)
for x, ax in zip(img_paths, axs.flatten()):
    img = np.asarray(Image.open(x))
    print(x)
    ax.axis('off')
    ax.set_title(x)
    ax.imshow(img)
fig.tight_layout(pad=.75)
plt.show()
print(f"{images.cursor * images.batch_size} of {images.units} images")

# %%

# %%
for i in range(100):
    print(i)

# %%
days = Record()
days.days
