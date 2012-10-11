# -*- coding: utf-8 -*-

from passbook import *
import uuid
import os
from datetime import datetime

def getTestPass():
    passId = "pass.com.yourdomain.pass"
    orgName = "Your organization"
    teamId = "Your Team ID" # from Apple

    p = Pass(Pass.EVENTTICKET, "test", orgName, passId, teamId, str(uuid.uuid4()))
    f = Field("test", "value", "test")
    p.addHeaderField(f)
    f.key = "test2"
    f.label = "xxxx33333"
    p.addPrimaryField(f)

    f = Field("key", "value", "label")
    p.addSecondaryField(f)

    p.setLocalizedString("zh-CN", 'label', "标签")

    imagename = 'icon.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'icon@2x.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'background.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'background@2x.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'thumbnail.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'thumbnail@2x.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'logo.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())
    imagename = 'logo@2x.png'
    p.setImage(imagename, open("images/" + imagename, 'r').read())

    p.setBackgroundColor(10, 10, 255)
    p.setForegroundColor(255, 255, 255)
    p.setLabelColor(255, 0, 0)
    p.logoText = "Your logo text"
    p.suppressStripShine = True

    p.addLocation(39.970562, 116.490353, None, 'CGV')

    p.setBarcode(Pass.PKBARCODE_FORMAT_QR, Pass.BARCODE_ENCODING_ISO_8859_1, "112325", "112325")

    p.relevantDate = '2012-10-10T16:01+08:00'

    f = Field("test time", p.relevantDate, "测试时间")
    p.addAuxiliaryField(f)

    DOUBAN_MOVIE_APP_STORE_ID = 446745748
    p.addAssociatedStoreIdentifier(DOUBAN_MOVIE_APP_STORE_ID)

    return p
