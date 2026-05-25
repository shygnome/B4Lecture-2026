# Exercise 3 Report

## Overview

In this exercise, an ablation study was conducted using different combinations of YOLO detectors and tracking methods in the TrackID3x3 notebook. The following combinations were compared:

* YOLO11x + ByteTrack
* YOLO11x + BoT-SORT
* YOLO11n + ByteTrack
* YOLO11n + BoT-SORT

The evaluation metrics used in this experiment were:

* TI-HOTA
* TI-DetA
* TI-AssA

## Result Summary

| Detector | Tracker   | TI-HOTA (%) ↑ | TI-DetA (%) ↑ | TI-AssA (%) ↑ |
| -------- | --------- | ------------: | ------------: | ------------: |
| YOLO11x  | ByteTrack |      **74.4** |      **73.7** |      **75.1** |
| YOLO11x  | BoT-SORT  |          74.1 |          73.3 |          74.8 |
| YOLO11n  | BoT-SORT  |          16.1 |          15.7 |          16.5 |
| YOLO11n  | ByteTrack |          25.8 |          23.7 |          28.1 |

## Discussion

Among all combinations, YOLO11x with ByteTrack achieved the best overall performance, obtaining the highest TI-HOTA, TI-DetA, and TI-AssA values. In contrast, YOLO11n with BoT-SORT produced the lowest performance.

Increasing the detector size from YOLO11n to YOLO11x significantly improved all evaluation metrics. In particular, TI-DetA improved substantially, suggesting that detection quality strongly affected the tracking performance.

Changing the tracker from ByteTrack to BoT-SORT resulted in only small differences when using YOLO11x. However, under the weaker YOLO11n detector, ByteTrack performed better than BoT-SORT.

These results suggest that detection performance was the primary challenge in this experiment. When the detector quality decreased, both detection accuracy and ID association performance deteriorated significantly. The visualization results also showed that weaker detector settings caused more unstable trajectories and tracking failures.

## Included Files

* `best_result_tracked_visualization.mp4`
* `worst_result_tracked_visualization.mp4`
* `ex3_summary_table.png`
