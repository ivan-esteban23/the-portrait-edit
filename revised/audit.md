# Issue 02 source audit

Audit performed before layout changes. All 174 studies, original prompts, titles, source links, and working notes remain intact. Visual findings are editorial flags, not identity claims or image corrections.

## Input and baseline inspection

- Reused the existing ReportLab generator: `scripts/build_issue_02.py` (baseline commit `940eaab`).
- Requested uploaded PDF path is unavailable. Inspected the matching existing 180-page repository PDF, also previously copied to Documents.
- `pdftotext -layout` confirms 180 letter-size pages, all 174 study numbers, titles, and Source filenames. Extracted text is saved in `current-pdf-layout.txt`.
- Requested `/mnt/user-data/outputs` directory cannot be created: permission denied. Revised deliverables use this directory and Documents instead.

## Potential image-prompt mismatches

These six visually identifiable mismatches retain their original filenames and images; each receives “Review pairing”.
- Study 7: 4991.jpg shows a mustard-yellow twist dress; the prompt describes a cream knit co-ord.
- Study 8: 4992.jpg shows a cream knit co-ord; the prompt describes a powder-blue knit set.
- Study 9: 4993.jpg shows a powder-blue knit set; the prompt describes a mustard twist dress.
- Study 12: 5030.jpg shows a black turtleneck, white mini and white socks; the prompt describes red polka-dot bows and a floral pinafore/blouse.
- Study 13: 5031.jpg shows a red headband and red puff-sleeve top; the prompt describes a black turtleneck and white mini.
- Study 14: 5032.jpg shows braids with red polka-dot bows and floral styling; the prompt describes a red headband and red puff sleeves.

Additional source wording issues retained verbatim:
- Study 44 title says “Camo Knit Skirt”, while its prompt/notes describe a cloud-like pattern. This is a title-versus-description discrepancy, not a confirmed swapped image.
- Study 115 notes refer to section 82, but its same-title/same-source counterpart is Study 83. The original note is preserved.
- Source notes sometimes suggest removing duplicates or shortening a prompt. Those notes remain verbatim; no such removal or shortening was performed.

## Duplicates and near-duplicates

All pages remain. Each member of every pair below receives “Repeats Study [N].” Exact matches are defined by shared Source filename or identical title; near matches are visually/source-note supported.
- Studies 79 / 106: same Source `24983.jpg` and same title.
- Studies 83 / 115: same Source `24984.jpg` and same title.
- Studies 113 / 126: same Source `25006.jpg` and same title.
- Studies 122 / 142: same Source `25023.jpg` and same title.
- Studies 48 / 75: near-duplicate. Different filenames show the same pink outfit/location; source notes explicitly call this a near-duplicate.
- Studies 62 / 66: near-duplicate. Same teahouse photograph/crop family; Study 66 explicitly describes the tighter view.
- Studies 69 / 76: near-duplicate. Same black-dress/lantern setting and apparent same photograph; source notes identify a near-duplicate.
- Studies 99 / 103: near-duplicate. Closely related monochrome polo-knit runway looks; source notes identify the alternate walk.
- Studies 147 / 152: near-duplicate. Same lilac mesh outfit in related views; source notes identify the alternate pose.

## Reference likeness and rights checks

All 170 unique references (all 174 study pages) are photographs or photorealistic portraits with visible, potentially recognizable people. No names, identities, authenticity, releases, ownership, or licenses can be established from these local files. Conservatively apply “Rights check” to every study, including repeated references; this is a review flag, not a claim that every image shows a known real person. The publisher decides. A complete study/filename list appears below.

## Cover count

174 studies and 170 unique reference filenames are consistent: four filenames occur twice (79/106, 83/115, 113/126, 122/142). Thus 174 - 4 = 170. Near-duplicates with different filenames do not change the unique-filename count.

## Small images

Threshold: short edge below 600 pixels. These may look soft at the fixed printed frame size. Preserve the original pixels; do not crop or resample upward.
- Study 36: `24373.jpg`, 368 × 552 px.
- Study 39: `24385.jpg`, 368 × 654 px.
- Study 42: `24381.jpg`, 368 × 654 px.
- Study 44: `24384.jpg`, 368 × 552 px.
- Study 50: `24392.jpg`, 368 × 548 px.
- Study 51: `24393.jpg`, 368 × 552 px.
- Study 52: `24391.jpg`, 525 × 700 px.
- Study 53: `24390.jpg`, 368 × 649 px.
- Study 54: `24376.jpg`, 368 × 550 px.
- Study 56: `24395.jpg`, 368 × 552 px.
- Study 57: `24402.jpg`, 368 × 654 px.
- Study 58: `24408.jpg`, 352 × 600 px.
- Study 60: `24413.jpg`, 368 × 548 px.
- Study 63: `24415.jpg`, 368 × 654 px.
- Study 64: `24411.jpg`, 368 × 552 px.
- Study 65: `24414.jpg`, 576 × 980 px.
- Study 67: `24404.jpg`, 368 × 654 px.
- Study 68: `24403.jpg`, 368 × 654 px.
- Study 70: `24410.jpg`, 368 × 675 px.
- Study 72: `24400.jpg`, 368 × 552 px.
- Study 73: `24405.jpg`, 368 × 552 px.
- Study 74: `24399.jpg`, 368 × 564 px.
- Study 97: `24989.jpg`, 400 × 600 px.
- Study 149: `25046.jpg`, 416 × 624 px.

## Complete rights-check inventory

| Study | Source | Original pixels | Review |
|---:|---|---|---|
| 1 | `4916.jpg` | 736 × 1308 | Rights check |
| 2 | `4564.jpg` | 720 × 881 | Rights check |
| 3 | `4570.jpg` | 640 × 813 | Rights check |
| 4 | `4571.jpg` | 736 × 981 | Rights check |
| 5 | `4572.jpg` | 736 × 1308 | Rights check |
| 6 | `4574.jpg` | 736 × 1308 | Rights check |
| 7 | `4991.jpg` | 736 × 981 | Rights check |
| 8 | `4992.jpg` | 736 × 981 | Rights check |
| 9 | `4993.jpg` | 666 × 999 | Rights check |
| 10 | `5028.jpg` | 736 × 981 | Rights check |
| 11 | `5029.jpg` | 736 × 981 | Rights check |
| 12 | `5030.jpg` | 736 × 1104 | Rights check |
| 13 | `5031.jpg` | 736 × 1313 | Rights check |
| 14 | `5032.jpg` | 736 × 985 | Rights check |
| 15 | `5088.jpg` | 736 × 1308 | Rights check |
| 16 | `5089.jpg` | 736 × 981 | Rights check |
| 17 | `24607.jpg` | 736 × 1308 | Rights check |
| 18 | `24603.jpg` | 736 × 1305 | Rights check |
| 19 | `24598.jpg` | 736 × 1318 | Rights check |
| 20 | `24604.jpg` | 736 × 985 | Rights check |
| 21 | `24606.jpg` | 735 × 985 | Rights check |
| 22 | `24600.jpg` | 736 × 1308 | Rights check |
| 23 | `24605.jpg` | 736 × 985 | Rights check |
| 24 | `24599.jpg` | 736 × 1308 | Rights check |
| 25 | `24572.jpg` | 735 × 980 | Rights check |
| 26 | `24573.jpg` | 700 × 990 | Rights check |
| 27 | `24547.jpg` | 736 × 906 | Rights check |
| 28 | `24570.jpg` | 736 × 981 | Rights check |
| 29 | `24537.jpg` | 736 × 977 | Rights check |
| 30 | `24548.jpg` | 735 × 735 | Rights check |
| 31 | `24535.jpg` | 736 × 1318 | Rights check |
| 32 | `24536.jpg` | 736 × 1104 | Rights check |
| 33 | `24533.jpg` | 736 × 918 | Rights check |
| 34 | `24546.jpg` | 720 × 720 | Rights check |
| 35 | `24534.jpg` | 714 × 1000 | Rights check |
| 36 | `24373.jpg` | 368 × 552 | Rights check |
| 37 | `24375.jpg` | 720 × 960 | Rights check |
| 38 | `24377.jpg` | 736 × 981 | Rights check |
| 39 | `24385.jpg` | 368 × 654 | Rights check |
| 40 | `24386.jpg` | 736 × 981 | Rights check |
| 41 | `24380.jpg` | 736 × 1000 | Rights check |
| 42 | `24381.jpg` | 368 × 654 | Rights check |
| 43 | `24387.jpg` | 683 × 1024 | Rights check |
| 44 | `24384.jpg` | 368 × 552 | Rights check |
| 45 | `24382.jpg` | 768 × 1024 | Rights check |
| 46 | `24388.jpg` | 736 × 978 | Rights check |
| 47 | `24383.jpg` | 736 × 928 | Rights check |
| 48 | `24389.jpg` | 768 × 1024 | Rights check |
| 49 | `24378.jpg` | 736 × 736 | Rights check |
| 50 | `24392.jpg` | 368 × 548 | Rights check |
| 51 | `24393.jpg` | 368 × 552 | Rights check |
| 52 | `24391.jpg` | 525 × 700 | Rights check |
| 53 | `24390.jpg` | 368 × 649 | Rights check |
| 54 | `24376.jpg` | 368 × 550 | Rights check |
| 55 | `24396.jpg` | 736 × 981 | Rights check |
| 56 | `24395.jpg` | 368 × 552 | Rights check |
| 57 | `24402.jpg` | 368 × 654 | Rights check |
| 58 | `24408.jpg` | 352 × 600 | Rights check |
| 59 | `24401.jpg` | 683 × 1024 | Rights check |
| 60 | `24413.jpg` | 368 × 548 | Rights check |
| 61 | `24407.jpg` | 736 × 981 | Rights check |
| 62 | `24412.jpg` | 768 × 1024 | Rights check |
| 63 | `24415.jpg` | 368 × 654 | Rights check |
| 64 | `24411.jpg` | 368 × 552 | Rights check |
| 65 | `24414.jpg` | 576 × 980 | Rights check |
| 66 | `24319.jpg` | 1536 × 2048 | Rights check |
| 67 | `24404.jpg` | 368 × 654 | Rights check |
| 68 | `24403.jpg` | 368 × 654 | Rights check |
| 69 | `24318.jpg` | 1528 × 2048 | Rights check |
| 70 | `24410.jpg` | 368 × 675 | Rights check |
| 71 | `24398.jpg` | 736 × 977 | Rights check |
| 72 | `24400.jpg` | 368 × 552 | Rights check |
| 73 | `24405.jpg` | 368 × 552 | Rights check |
| 74 | `24399.jpg` | 368 × 564 | Rights check |
| 75 | `24317.jpg` | 1536 × 2048 | Rights check |
| 76 | `24409.jpg` | 764 × 1024 | Rights check |
| 77 | `24969.jpg` | 736 × 1308 | Rights check |
| 78 | `24982.jpg` | 736 × 1104 | Rights check |
| 79 | `24983.jpg` | 736 × 981 | Rights check |
| 80 | `24981.jpg` | 736 × 981 | Rights check |
| 81 | `24970.jpg` | 736 × 989 | Rights check |
| 82 | `24976.jpg` | 735 × 1006 | Rights check |
| 83 | `24984.jpg` | 736 × 900 | Rights check |
| 84 | `24966.jpg` | 720 × 1600 | Rights check |
| 85 | `24967.jpg` | 736 × 1258 | Rights check |
| 86 | `24968.jpg` | 736 × 1104 | Rights check |
| 87 | `24975.jpg` | 736 × 736 | Rights check |
| 88 | `24974.jpg` | 736 × 978 | Rights check |
| 89 | `24965.jpg` | 736 × 1475 | Rights check |
| 90 | `24972.jpg` | 735 × 977 | Rights check |
| 91 | `24971.jpg` | 736 × 981 | Rights check |
| 92 | `24978.jpg` | 736 × 981 | Rights check |
| 93 | `24980.jpg` | 735 × 997 | Rights check |
| 94 | `24973.jpg` | 736 × 978 | Rights check |
| 95 | `24979.jpg` | 736 × 1073 | Rights check |
| 96 | `24977.jpg` | 713 × 1070 | Rights check |
| 97 | `24989.jpg` | 400 × 600 | Rights check |
| 98 | `24991.jpg` | 736 × 920 | Rights check |
| 99 | `25000.jpg` | 736 × 920 | Rights check |
| 100 | `24996.jpg` | 682 × 1026 | Rights check |
| 101 | `25004.jpg` | 736 × 977 | Rights check |
| 102 | `24992.jpg` | 736 × 920 | Rights check |
| 103 | `25002.jpg` | 640 × 853 | Rights check |
| 104 | `25005.jpg` | 736 × 729 | Rights check |
| 105 | `24990.jpg` | 736 × 1308 | Rights check |
| 106 | `24983.jpg` | 736 × 981 | Rights check |
| 107 | `24994.jpg` | 736 × 920 | Rights check |
| 108 | `25001.jpg` | 736 × 1104 | Rights check |
| 109 | `24993.jpg` | 736 × 920 | Rights check |
| 110 | `24997.jpg` | 736 × 981 | Rights check |
| 111 | `25003.jpg` | 736 × 981 | Rights check |
| 112 | `24999.jpg` | 677 × 1200 | Rights check |
| 113 | `25006.jpg` | 736 × 1308 | Rights check |
| 114 | `24998.jpg` | 736 × 981 | Rights check |
| 115 | `24984.jpg` | 736 × 900 | Rights check |
| 116 | `24995.jpg` | 674 × 1200 | Rights check |
| 117 | `25007.jpg` | 736 × 1308 | Rights check |
| 118 | `25024.jpg` | 736 × 1308 | Rights check |
| 119 | `25025.jpg` | 736 × 1308 | Rights check |
| 120 | `25015.jpg` | 736 × 1308 | Rights check |
| 121 | `25016.jpg` | 736 × 1217 | Rights check |
| 122 | `25023.jpg` | 736 × 1308 | Rights check |
| 123 | `25013.jpg` | 736 × 1308 | Rights check |
| 124 | `25017.jpg` | 736 × 1104 | Rights check |
| 125 | `25010.jpg` | 675 × 1200 | Rights check |
| 126 | `25006.jpg` | 736 × 1308 | Rights check |
| 127 | `25012.jpg` | 736 × 1308 | Rights check |
| 128 | `25014.jpg` | 675 × 1200 | Rights check |
| 129 | `25011.jpg` | 736 × 1308 | Rights check |
| 130 | `25009.jpg` | 736 × 1308 | Rights check |
| 131 | `25008.jpg` | 736 × 1308 | Rights check |
| 132 | `25018.jpg` | 736 × 1152 | Rights check |
| 133 | `25019.jpg` | 736 × 1270 | Rights check |
| 134 | `25020.jpg` | 736 × 1308 | Rights check |
| 135 | `25021.jpg` | 736 × 1308 | Rights check |
| 136 | `25022.jpg` | 736 × 1308 | Rights check |
| 137 | `25028.jpg` | 720 × 1080 | Rights check |
| 138 | `25033.jpg` | 736 × 1308 | Rights check |
| 139 | `25034.jpg` | 736 × 977 | Rights check |
| 140 | `25032.jpg` | 736 × 1308 | Rights check |
| 141 | `25048.jpg` | 736 × 981 | Rights check |
| 142 | `25023.jpg` | 736 × 1308 | Rights check |
| 143 | `25030.jpg` | 736 × 981 | Rights check |
| 144 | `25050.jpg` | 736 × 981 | Rights check |
| 145 | `25026.jpg` | 600 × 900 | Rights check |
| 146 | `25047.jpg` | 736 × 981 | Rights check |
| 147 | `25043.jpg` | 736 × 981 | Rights check |
| 148 | `25029.jpg` | 736 × 1308 | Rights check |
| 149 | `25046.jpg` | 416 × 624 | Rights check |
| 150 | `25045.jpg` | 736 × 983 | Rights check |
| 151 | `25044.jpg` | 674 × 1200 | Rights check |
| 152 | `25027.jpg` | 736 × 981 | Rights check |
| 153 | `25049.jpg` | 720 × 1000 | Rights check |
| 154 | `25031.jpg` | 736 × 1306 | Rights check |
| 155 | `25058.jpg` | 681 × 1142 | Rights check |
| 156 | `25071.jpg` | 736 × 920 | Rights check |
| 157 | `25055.jpg` | 736 × 981 | Rights check |
| 158 | `25070.jpg` | 736 × 920 | Rights check |
| 159 | `25068.jpg` | 736 × 981 | Rights check |
| 160 | `25069.jpg` | 736 × 988 | Rights check |
| 161 | `25061.jpg` | 736 × 1308 | Rights check |
| 162 | `25062.jpg` | 736 × 1308 | Rights check |
| 163 | `25057.jpg` | 736 × 1308 | Rights check |
| 164 | `25051.jpg` | 736 × 981 | Rights check |
| 165 | `25053.jpg` | 736 × 981 | Rights check |
| 166 | `25064.jpg` | 736 × 1137 | Rights check |
| 167 | `25060.png` | 1024 × 1536 | Rights check |
| 168 | `25054.jpg` | 736 × 981 | Rights check |
| 169 | `25063.jpg` | 736 × 1308 | Rights check |
| 170 | `25067.jpg` | 676 × 1200 | Rights check |
| 171 | `25052.jpg` | 736 × 981 | Rights check |
| 172 | `25066.jpg` | 736 × 1308 | Rights check |
| 173 | `25056.jpg` | 736 × 981 | Rights check |
| 174 | `25065.jpg` | 736 × 1010 | Rights check |
