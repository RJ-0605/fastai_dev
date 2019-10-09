#AUTOGENERATED! DO NOT EDIT! File to edit: dev/14a_callback_data.ipynb (unless otherwise specified).

__all__ = ['CollectDataCallback', 'WeightedSampleCallback', 'weighted_sampler']

#Cell
from ..torch_basics import *
from ..test import *
from ..layers import *
from ..data.all import *
from ..optimizer import *
from ..learner import *

#Cell
class CollectDataCallback(Callback):
    "Collect all batches, along with `pred` and `loss`, into `self.data`"
    def begin_fit(self): self.data = L()
    def after_batch(self): self.data.append(to_detach(to_cpu((self.xb,self.yb,self.pred,self.loss))))

#Cell
class WeightedSampleCallback(Callback):
    "Use weighted sampling in `DataLoader`"
    run_after=TrainEvalCallback

    def __init__(self, wgts, learn=None):
        self.set_wgts(wgts)
        self.learn = learn

    def set_wgts(self, wgts):
        wgts = array(wgts)
        self.wgts = wgts/wgts.sum()

    def get_idxs(self):
        n = self.dl.n
        return list(np.random.choice(n, n, p=self.wgts))

    def begin_fit(self):
        self.old_getidx = self.dl.get_idxs
        self.dl.get_idxs = self.get_idxs

    def after_fit(self): self.dl.get_idxs = self.old_getidx

    @property
    def dl(self): return self.learn.dbunch.train_dl

#Cell
@patch
def weighted_sampler(self:Learner, wgts):
    self.add_cb(WeightedSampleCallback(wgts))
    return self