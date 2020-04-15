import chardet
import codecs
#f = open(u'加解密.md','rb')
# f = open(u'加解密1.md','rb')
# #f = open(u'Python笔记.md','rb')
# data = f.read()
# print(chardet.detect(data))
import os


def utf16le2utf8(filename):
    filename = u'钟爱的文字.md'
    # filename = u'加解密.md'

    with open(filename, 'rb') as file:
        content = file.read()
        print(content)

    with open(filename, 'rb') as binaryfile:
        charset = chardet.detect(binaryfile.read())
        print(charset)
        
    decoder = codecs.getdecoder('utf_8')
    print(decoder(content)[0])
    decoder = codecs.getdecoder('utf_16_le')
    print(decoder(content)[0])
    # if decoder:
    #     print(decoder(content)[0])
        # with open(filename, 'w', encoding='utf-8') as utf8_file:
        #     utf8_file.write(decoder(content)[0])
        # pass

utf16le2utf8('')