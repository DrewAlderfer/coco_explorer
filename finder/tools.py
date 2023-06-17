import os
import pprint as pp
from typing import Self
import numpy as np
import polars as pb
import matplotlib.pyplot as plt
from pycocotools.coco import COCO

pp.PrettyPrinter(indent=4, width=60)

def group_anns(anns, ann_param:str="caption"):
    """
    Groups a list of COCO annotation dicts into lists of annotations with matching `image_id`s
    """
    ann_groups = {}
    for ann in anns:
        try:
            ann_groups[ann['image_id']].append(ann[ann_param])
            continue
        except KeyError:
            ann_groups.update({ann['image_id']: [ann[ann_param]]})
    return ann_groups

class Search_Result(list):
    def __init__(self, results, batch_size:int=12):
        self.results = results
        self.batch_size = batch_size
        batch_count, last = divmod(len(self.results), self.batch_size)
        self.cursor = 0
        self.output = []
        dir_path = "./data/train2017/"
        for batch in range(batch_count):
            start = batch * self.batch_size
            end = start + self.batch_size
            img_paths = [f"{dir_path}{img:012d}.jpg" for img in self.results[start:end]]
            self.output.append(img_paths)
        if last > 0:
            self.output.append([f"{dir_path}{img:012d}.jpg" for img in self.results[-last:]])
        self.units = self.batch_size * batch_count + last if batch_count > 0 else last

    def _fmt_block(self, fmt_str, idx=0):
        fmt_str += "  [\n"
        for i in range(2):
            fmt_str += f"  [{i}]='{self.output[idx][i]}'\n"
        if len(self.output[idx]) > 3:
            fmt_str += "  ...\n"
        if len(self.output[idx]) > 2:
            fmt_str += f"  [{len(self.output[idx]) - 1}]='{self.output[idx][-1]}'\n"
        fmt_str += "  ]\n"
        return fmt_str

    def __str__(self):
        fmt_str = "[\n"
        fmt_str = self._fmt_block(fmt_str)
        if len(self) > 1:
            fmt_str += "...\n"
            fmt_str = self._fmt_block(fmt_str, -1)
        fmt_str += "]"
        fmt_str += f" <type=COCO_Image_Search, batches={len(self)}, images={self.units}]>"
        return fmt_str

    def __len__(self) -> int:
        return len(self.output)

    def __iter__(self):
        self.cursor = 0
        return self

    def __next__(self):
        if self.cursor < len(self):
            x = self.output[self.cursor]
            self.cursor += 1
            return x
        else:
            raise StopIteration

class COCO_Image_Search():
    def __init__(self,
                 data_dir= './finder/static/data',
                 ann_file = '/annotations/instances_train2017.json',
                 img_dir = '/train2017',
                 caps_annFile = '/annotations/captions_train2017.json'):
        self.img_dir = f"{data_dir}{img_dir}"
        self.coco = COCO(f"{data_dir}{ann_file}")
        self.coco_caps = COCO(f"{data_dir}{caps_annFile}")
        self.imgs = None
        self.search_results = None

    def get_results(self):
        if self.search_results:
            return Search_Result(self.search_results)
        if self.imgs:
            return Search_Result(self.imgs)
        raise Exception("No search results to return!") from ValueError

    def cat_search(self, cats:list=['person', 'dog']) -> Self:

        catIds = self.coco.getCatIds(catNms=cats)
        self.img_ids = self.coco.getImgIds(catIds=catIds)
        self.imgs = self.coco.loadImgs(self.img_ids)
        return self
        
    def caption_contains(self, terms:list[str]) -> Self:
        capIds = self.coco_caps.getAnnIds(imgIds=self.img_ids)
        caps = self.coco_caps.loadAnns(capIds)
        df = pb.DataFrame(caps)
        pattern = terms.pop(0)
        if len(terms) > 0:
            for word in terms:
                pattern += f"|{word}"
        print(pattern)

        self.search_results = df.filter(pb.col('caption').str.contains(pattern))['image_id'].unique().to_list()

        return self

