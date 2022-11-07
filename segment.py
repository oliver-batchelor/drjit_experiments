from typing import Tuple

import drjit as dr
import matplotlib.pyplot as plt
from drjit.cuda.ad import Array3f, Float, Loop, UInt32

from geometry_types import AABox, Segment, Tubelet


def point_segment_dist(p:Array3f, seg:Segment, 
  eps:Float=1e-6) -> Tuple[Float, Float]:

  d = seg.b - seg.a
  l2 = dr.dot(d, d)  # |b - a|^2

  t = dr.clamp(dr.dot(d, (p - seg.a) / l2), 0., 1.)
  p_proj = seg.a + t * d
  delta_p = p_proj - p

  dist_sq = dr.dot(delta_p, delta_p)
  pb = p - seg.b

  dist_sq = dr.select(l2 >= eps, dist_sq, dr.dot(pb, pb))
  return t, dist_sq


def segment_box(box:AABox, seg:Segment):
  dir = seg.b - seg.a

  a_start = (box.min - seg.a) / dir
  a_end = (box.max - seg.a) / dir 

  b_start = (seg.b - box.min) / dir
  b_end = (seg.b - box.max) / dir 

  return  (dr.minimum(a_start, a_end),  
    1 - dr.minimum(b_start, b_end))


def seg_seg_nearest(seg1:Segment, seg2:Segment, eps=1e-6) -> Tuple[Float, Float]:
  v21 = seg2.a - seg1.a
    
  proj21 = dr.dot(seg2.dir, seg1.dir)
  proj21_1 = dr.dot(v21, seg1.dir)
  proj21_2 = dr.dot(v21, seg2.dir)

  denom = proj21 * proj21 - seg2.length_sq * seg1.length_sq
  t1 = proj21_1 / proj21

  s2 = (proj21_2 * proj21 - seg2.length_sq * proj21_1) / denom
  t2 = (-proj21_1 * proj21 + seg1.length_sq * proj21_2) / denom

  nz = dr.abs(denom) < eps
  s = dr.select(nz, 0, s2)
  t = dr.select(nz, t1, t2)
  return dr.clamp(s, 0, 1), dr.clamp(t, 0, 1)


def seg_seg_dist(seg1:Segment, seg2:Segment) -> Float:
  s, t = seg_seg_nearest(seg1, seg2)
  p1 = seg1.a + s * seg1.dir
  p2 = seg2.a + t * seg2.dir
  
  return dr.sqrt(dr.dot(p1 - p2, p1 - p2))


# def distance_matrix(f, x, y):

#   min_dist = Float(0.0)
#   i = UInt32(0)
  
#   loop = Loop("Distance", lambda: (i, min_dist))
#   while loop(i < y.width):
