# -*- coding: utf-8 -*-
# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

from unittest import TestCase, main
from lucene import ThaiAnalyzer, ThaiWordFilter, StringReader, Version
from BaseTokenStreamTestCase import BaseTokenStreamTestCase


class ThaiAnalyzerTestCase(BaseTokenStreamTestCase):

    def testOffsets(self):
        self.assertTrue(ThaiWordFilter.DBBI_AVAILABLE,
                     "JRE does not support Thai dictionary-based BreakIterator")
        self._assertAnalyzesTo(ThaiAnalyzer(Version.LUCENE_35),
                               "การที่ได้ต้องแสดงว่างานดี", 
                               [ "การ", "ที่", "ได้", "ต้อง", "แสดง",
                                 "ว่า", "งาน", "ดี" ],
                               [ 0, 3, 6, 9, 13, 17, 20, 23 ],
                               [ 3, 6, 9, 13, 17, 20, 23, 25 ])

    def testTokenType(self):
        self.assertTrue(ThaiWordFilter.DBBI_AVAILABLE,
                     "JRE does not support Thai dictionary-based BreakIterator")

        self._assertAnalyzesTo(ThaiAnalyzer(Version.LUCENE_35),
                               "การที่ได้ต้องแสดงว่างานดี ๑๒๓", 
                               [ "การ", "ที่", "ได้", "ต้อง", "แสดง",
                                 "ว่า", "งาน", "ดี", "๑๒๓" ],
                               None, None,
                               [ "<SOUTHEAST_ASIAN>", "<SOUTHEAST_ASIAN>", 
                                 "<SOUTHEAST_ASIAN>", "<SOUTHEAST_ASIAN>", 
                                 "<SOUTHEAST_ASIAN>", "<SOUTHEAST_ASIAN>",
                                 "<SOUTHEAST_ASIAN>", "<SOUTHEAST_ASIAN>",
                                 "<NUM>" ])

    def testPositionIncrements(self):
        self.assertTrue(ThaiWordFilter.DBBI_AVAILABLE,
                     "JRE does not support Thai dictionary-based BreakIterator")

        analyzer = ThaiAnalyzer(Version.LUCENE_35)

        self._assertAnalyzesTo(analyzer, "การที่ได้ต้อง the แสดงว่างานดี", 
                               [ "การ", "ที่", "ได้", "ต้อง", "แสดง",
                                 "ว่า", "งาน", "ดี" ],
                               [ 0, 3, 6, 9, 18, 22, 25, 28 ],
                               [ 3, 6, 9, 13, 22, 25, 28, 30 ],
                               None,
                               [ 1, 1, 1, 1, 2, 1, 1, 1 ])
	 
        # case that a stopword is adjacent to thai text, with no whitespace
        self._assertAnalyzesTo(analyzer, "การที่ได้ต้องthe แสดงว่างานดี", 
                               [ "การ", "ที่", "ได้", "ต้อง", "แสดง",
                                 "ว่า", "งาน", "ดี" ],
                               [ 0, 3, 6, 9, 17, 21, 24, 27 ],
                               [ 3, 6, 9, 13, 21, 24, 27, 29 ],
                               None,
                               [ 1, 1, 1, 1, 2, 1, 1, 1 ])

    def testAnalyzer30(self):

        analyzer = ThaiAnalyzer(Version.LUCENE_30)
    
        self._assertAnalyzesTo(analyzer, "", [])

        self._assertAnalyzesTo(analyzer,
                               "การที่ได้ต้องแสดงว่างานดี",
                               [ "การ", "ที่", "ได้", "ต้อง",
                                 "แสดง", "ว่า", "งาน", "ดี" ])

        self._assertAnalyzesTo(analyzer,
                               "บริษัทชื่อ XY&Z - คุยกับ xyz@demo.com",
                               [ "บริษัท", "ชื่อ", "xy&z", "คุย", "กับ", "xyz@demo.com" ])

        # English stop words
        self._assertAnalyzesTo(analyzer,
                               "ประโยคว่า The quick brown fox jumped over the lazy dogs",
                               [ "ประโยค", "ว่า", "quick", "brown", "fox",
                                 "jumped", "over", "lazy", "dogs" ])


if __name__ == "__main__":
    import sys, lucene
    lucene.initVM()
    if ThaiWordFilter.DBBI_AVAILABLE:
        if '-loop' in sys.argv:
            sys.argv.remove('-loop')
            while True:
                try:
                    main()
                except:
                    pass
        else:
            main()
    else:
        print("Thai not supported by this JVM, tests skipped", file=sys.stderr)
