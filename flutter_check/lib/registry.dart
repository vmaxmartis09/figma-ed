import 'package:flutter/widgets.dart';
import 'gen/s01.dart';
import 'gen/s02.dart';
import 'gen/s03.dart';
import 'gen/s04.dart';
import 'gen/s05.dart';
import 'gen/s06.dart';
import 'gen/s07.dart';
import 'gen/s08.dart';
import 'gen/s09.dart';
import 'gen/s10.dart';
import 'gen/s11.dart';
import 'gen/s12.dart';
import 'gen/s13.dart';
import 'gen/s14.dart';
import 'gen/s15.dart';
import 'gen/s16.dart';
import 'gen/s17.dart';
import 'gen/s18.dart';
import 'gen/s19.dart';
import 'gen/s20.dart';
import 'gen/s21.dart';
import 'gen/s22.dart';

final imagePaths = <String>['/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/01_Video&Course - Videos/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/01_Video&Course - Videos/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/01_Video&Course - Videos/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/01_Video&Course - Videos/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/01_Video&Course - Videos/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/02_Video&Course - Video/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/02_Video&Course - Video/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/02_Video&Course - Video/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/02_Video&Course - Video/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/02_Video&Course - Video/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/04_Video&Course - Video- search_2/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/06_Video&Course - filter/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/06_Video&Course - filter/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/06_Video&Course - filter/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/06_Video&Course - filter/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/06_Video&Course - filter/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/07_Video&Course - Videos_2/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/07_Video&Course - Videos_2/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/07_Video&Course - Videos_2/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/07_Video&Course - Videos_2/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/07_Video&Course - Videos_2/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/08_Video Detail/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/08_Video Detail/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/08_Video Detail/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/08_Video Detail/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/08_Video Detail/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/06.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/07.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/08.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/11_Recommended Video detail - cmt/images/09.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/06.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/07.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/08.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/12_Recommended Video detail - cmt_2/images/09.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/13_Video&Course - Watch History/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/13_Video&Course - Watch History/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/16_Video&Course - VideoDownload/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/16_Video&Course - VideoDownload/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/17_Video&Course - VideoDownload_2/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/17_Video&Course - VideoDownload_2/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/18_Video&Course - VideoDownload_3/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/18_Video&Course - VideoDownload_3/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/19_Video&Course - VideoDownload_4/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/19_Video&Course - VideoDownload_4/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/20_Video&Course - VideoDownload_5/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/20_Video&Course - VideoDownload_5/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/20_Video&Course - VideoDownload_5/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/21_Video&Course - Videos_3/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/21_Video&Course - Videos_3/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/21_Video&Course - Videos_3/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/21_Video&Course - Videos_3/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/21_Video&Course - Videos_3/images/05.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/22_Video Detail_4/images/01.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/22_Video Detail_4/images/02.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/22_Video Detail_4/images/03.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/22_Video Detail_4/images/04.png', '/Volumes/Data/figma-ediva/FC-Mobile Design/Videos/_story/screens/22_Video Detail_4/images/05.png'];
final screens = <(String, double, double, Widget Function())>[
  ('S01', 375.0, 980.0, () => const S01()),
  ('S02', 375.0, 980.0, () => const S02()),
  ('S03', 375.0, 815.0, () => const S03()),
  ('S04', 375.0, 815.0, () => const S04()),
  ('S05', 375.0, 815.0, () => const S05()),
  ('S06', 375.0, 815.0, () => const S06()),
  ('S07', 375.0, 980.0, () => const S07()),
  ('S08', 375.0, 1435.0, () => const S08()),
  ('S09', 375.0, 815.0, () => const S09()),
  ('S10', 375.0, 815.0, () => const S10()),
  ('S11', 375.0, 1274.0, () => const S11()),
  ('S12', 375.0, 815.0, () => const S12()),
  ('S13', 375.0, 903.0, () => const S13()),
  ('S14', 375.0, 815.0, () => const S14()),
  ('S15', 375.0, 815.0, () => const S15()),
  ('S16', 375.0, 815.0, () => const S16()),
  ('S17', 375.0, 815.0, () => const S17()),
  ('S18', 375.0, 815.0, () => const S18()),
  ('S19', 375.0, 815.0, () => const S19()),
  ('S20', 375.0, 815.0, () => const S20()),
  ('S21', 375.0, 980.0, () => const S21()),
  ('S22', 375.0, 815.0, () => const S22())
];
