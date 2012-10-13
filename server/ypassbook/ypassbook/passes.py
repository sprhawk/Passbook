# -*- coding: utf-8 -*-
# 
# Copyright (c) 2012, Hongbo Yang (hongbo@yang.me)
# All rights reserved.
# 
# 1. Redistribution and use in source and binary forms, with or without modification, are permitted 
# provided that the following conditions are met:
# 
# 2. Redistributions of source code must retain the above copyright notice, this list of conditions 
# and 
# the following disclaimer.
# 
# 3. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
# and the following disclaimer in the documentation and/or other materials provided with the 
# distribution.
# 
# Neither the name of the Hongbo Yang nor the names of its contributors may be used to endorse or 
# promote products derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#hongbo@yang.me
#2012/10/08

import json
import os
import hashlib
from M2Crypto import SMIME
from M2Crypto import X509
from M2Crypto.X509 import X509_Stack
from zipfile import ZipFile
import cStringIO

class Pass:
    """
    Create a template for Apple Passbook structure
    """
    WHITE_LISTS = ["pass.json", "pass.strings", "icon.png", "icon@2x.png", "background.png", 
                   "background@2x.png", "footer.png", "footer@2x.png", "logo.png", "logo@2x.png",
                   "strip.png", "strip@2x.png", "thumbnail.png", "thumbnail@2x.png"]


    BOARDINGPASS = "boardingPass"
    COUPON = "COUPON"
    EVENTTICKET = "eventTicket"
    GENERIC = "generic"
    STORECARD = "storecard"


    PKTRANSIT_TYPE_AIR = "PKTransitTypeAir"
    PKTRANSIT_TYPE_BOAT = "PKTransitTypeBoat"
    PKTRANSIT_TYPE_BUS = "PKTransitTypeBus"
    PKTRANSIT_TYPE_GENERIC = "PKTransitTypeGeneric"
    PKTRANSIT_TYPE_TRAIN = "PKTransitTypeTrain"

    PKBARCODE_FORMAT_QR = "PKBarcodeFormatQR"
    PKBARCODE_FORMAT_PDF417 = "PKBarcodeFormatPDF417"
    PKBARCODE_FORMAT_AZTEC = "PKBarcodeFormatAztec"
    
    BARCODE_ENCODING_ISO_8859_1 = "iso-8859-1"

    def __init__(self, type, description, organizationName, passTypeIdentifier, teamIdentifier, serialNumber, formatVersion = 1):
        self.type = type

        #required fields
        self.description = description #localizable
        self.organizationName = organizationName #localizable
        self.passTypeIdentifier = passTypeIdentifier
        self.serialNumber = serialNumber
        self.teamIdentifier = teamIdentifier
        self.formatVersion = formatVersion

        #optional fields
        self.associatedStoreIdentifiers = None # [] must be number
        self.locations = None # []
        self.relevantDate = None #ISO 8601 date, as a string
        """2012-10-10 上午2:09:23.697 MobileSafari[80785]: Invalid data error reading card pass.com.douban.movie.ticket/aa454fc8-0465-490d-9cdd-96fda1337713. Unable to parse relevantDate 2012-10-10T02:09:17 as a date. We expect dates in "W3C date time stamp format", either "Complete date plus hours and minutes" or "Complete date plus hours, minutes and seconds". For example, 1980-05-07T10:30-05:00.
        """

        #style keys
        self.styleKeys = None #boardingPass/coupon/eventTicket/generic/storeCard

        self.transitType = None

        #Visual Appearance Keys
        self.barcode = None #{}
        self.backgroundColor = None # rgb(0,0,0)
        self.foregroundColor = None #
        self.labelColor = None
        self.logoText = None
        self.suppressStripShine = None
        self.authenticationToken = None
        self.webServiceURL = None

        self.localizedStrings = {}
        self.localizedImages = {}
        self.images = {}

        self.fieldsKeys = []

    #data manipulation
    def addFieldToStyleKey(self, styleKey, field):
        if field.key in self.fieldsKeys:
            raise ValueError # cannot use same key in fields
        self.fieldsKeys.append(field.key)
        if not self.styleKeys:
            self.styleKeys = {}

        if styleKey not in self.styleKeys:
            self.styleKeys[styleKey] = []
        self.styleKeys[styleKey].append(field.getDict())

    def addHeaderField(self, field):
        self.addFieldToStyleKey('headerFields', field)
    def addPrimaryField(self, field):
        self.addFieldToStyleKey('primaryFields', field)
    def addSecondaryField(self, field):
        self.addFieldToStyleKey('secondaryFields', field)
    def addAuxiliaryField(self, field):
        self.addFieldToStyleKey('auxiliaryFields', field)
    def addBackField(self, field):
        self.addFieldToStyleKey('backFields', field)

    def setImage(self, name, imagedata):
        if name in Pass.WHITE_LISTS:
            self.images[name] = imagedata
        else:
            raise ValueError

    def setLocalizedImage(self, locale, name, imagedata):
        if name in WHITE_LISTS:
            if not locale in self.localizedImages:
                self.localizedImages[locale] = {}
            self.localizedImages[locale][name] = imagedata
        else:
            raise ValueError #how to add message?

    def setLocalizedString(self, locale, label, string):
        if not locale in self.localizedStrings:
            self.localizedStrings[locale] = {}
        self.localizedStrings[locale][label] = string

    def addLocation(self, latitude, longitude, altitude = None, relevantText = None):
        location = {}
        location['latitude'] = float(latitude)
        location['longitude'] = float(longitude)
        if altitude:
            location['altitude'] = float(altitude)
        if relevantText:
            location['relevantText'] = relevantText
        if not self.locations:
            self.locations = []
        self.locations.append(location)

    def setBarcode(self, format, encoding, message, altText = None):
        if not self.barcode:
            self.barcode = {}
        self.barcode["format"] = format
        self.barcode["messageEncoding"] = encoding
        self.barcode['message'] = message
        if altText:
            self.barcode['altText'] = altText

    def rgbString(self, r, g, b):
        return "rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")"

    def setBackgroundColor(self, r, g, b):
        self.backgroundColor = self.rgbString(r, g, b)
    def setForegroundColor(self, r, g, b):
        self.foregroundColor = self.rgbString(r, g, b)
    def setLabelColor(self, r, g, b):
        self.labelColor = self.rgbString(r, g, b)
    def addAssociatedStoreIdentifier(self, identifier):
        if not self.associatedStoreIdentifiers:
            self.associatedStoreIdentifiers = []
        self.associatedStoreIdentifiers.append(int(identifier))

    #get package info
    def getPassJson(self):
        return json.dumps(self.getDict(), indent=4)

    def getDict(self): 
        pass_dict = {}
        #required fields
        pass_dict['description'] = self.description #localizable
        pass_dict['formatVersion'] = self.formatVersion
        pass_dict['organizationName'] = self.organizationName #localizable
        pass_dict['passTypeIdentifier'] = self.passTypeIdentifier
        pass_dict['serialNumber'] = self.serialNumber
        pass_dict['teamIdentifier'] = self.teamIdentifier

        #optional fields
        if self.associatedStoreIdentifiers:
            pass_dict['associatedStoreIdentifiers'] = self.associatedStoreIdentifiers

        if self.locations:
            pass_dict['locations'] = self.locations

        if self.relevantDate:
            pass_dict['relevantDate'] = self.relevantDate

        #no value checks
        if self.styleKeys:
            if self.type == Pass.BOARDINGPASS and "transitType" not in self.styleKeys:
                self.styleKeys['transitType'] = self.PKTRANSIT_TYPE_GENERIC
            pass_dict[self.type] = self.styleKeys

        #Visual Appearance Keys
        if self.barcode:
            pass_dict['barcode'] = self.barcode

        if self.backgroundColor:
            pass_dict['backgroundColor'] = self.backgroundColor
        if self.foregroundColor:
            pass_dict['foregroundColor'] = self.foregroundColor
        if self.labelColor:
            pass_dict['labelColor'] = self.labelColor
        if self.logoText:
            pass_dict['logoText'] = self.logoText
        if self.suppressStripShine:
            pass_dict['suppressStripShine'] = self.suppressStripShine

        #Web Service Keys
        if self.authenticationToken and self.webServiceURL:
            pass_dict['authenticationToken'] = self.authenticationToken
            pass_dict['webServiceURL'] = self.webServiceURL

        return pass_dict

    def __repr__(self):
        return repr(self.getDict())

    def hexhash(self, data):
        hash = hashlib.sha1()
        hash.update(data)
        return hash.hexdigest()

    def getLocalizedStrings(self):
        localizedStrings = {}
        for locale, strings in self.localizedStrings.iteritems():
            localepath = locale+'.lproj/pass.strings'
            locales = ""
            for label, string in strings.iteritems():
                locales = locales + ('"' + label + '"="' + string + '";' + "\n" )
            localizedStrings[localepath] = locales
        return localizedStrings

    def getPackage(self):
        package = {}
        manifest = {}

        data = self.getPassJson()
        hash = self.hexhash(data)
        package["pass.json"] = data
        manifest["pass.json"] = hash

        #normal images
        for name, data in self.images.iteritems():
            hash = self.hexhash(data)
            package[name] = data
            manifest[name] = hash
        
        #localized strings
        s = self.getLocalizedStrings()
        for localepath, strings in s.iteritems():
            hash = self.hexhash(strings)
            package[localepath] = strings
            manifest[localepath] = hash

        #localized images
        for locale, images in self.localizedImages.iteritems():
            localename = locale+'.lproj/'
            for name, data in images.iteritems():
                hash = self.hexhash(data)
                package[localename + name] = data
                manifest[localename + name] = hash

        manifestdata = json.dumps(manifest, indent=4)
        package["manifest.json"] = manifestdata
        return package

    def savePackage(self, path = None):
        package = self.getPackage()
        if not path:
            path = self.passTypeIdentifier + self.serialNumber + ".pass"
        if os.path.exists(path):
            raise OSError

        os.mkdir(path)
        for filepath, data in package.iteritems():
            splits = filepath.split('/')
            if 1 != len(splits) or "" != splits[0]:
                i = 0
                subpath = path
                for i in range(len(splits) - 1):
                    subpath = os.path.join(subpath, splits[i])
                    os.mkdir(subpath)
                    
            p = os.path.join(path, filepath)
            open(p, 'w').write(data)

    def sign(self, data, wwdrcert_data, cert_data, key_data, passphrase = None):
        """ https://github.com/devartis/passbook """
        def passwordCallback(*args, **kwds):
            return passphrase
        wwdrcert_bio = SMIME.BIO.MemoryBuffer(wwdrcert_data)
        key_bio = SMIME.BIO.MemoryBuffer(key_data)
        cert_bio = SMIME.BIO.MemoryBuffer(cert_data)

        smime = SMIME.SMIME()
        wwdrcert = X509.load_cert_bio(wwdrcert_bio)
        stack = X509_Stack()
        stack.push(wwdrcert)
        smime.set_x509_stack(stack)
        smime.load_key_bio(key_bio, cert_bio, callback=passwordCallback)
        pk7 = smime.sign(SMIME.BIO.MemoryBuffer(data), flags = SMIME.PKCS7_DETACHED | SMIME.PKCS7_BINARY)
        pem = SMIME.BIO.MemoryBuffer()
        pk7.write(pem)
        der = ''.join(l.strip() for l in pem.read().split('----')[2].splitlines()).decode('base64')
        return der

    def zipPackage(self, package):
        buffer = cStringIO.StringIO()
        with ZipFile(buffer, 'w') as zip:
            for filepath, data in package.iteritems():
                zip.writestr(filepath, data)
        zipdata = buffer.getvalue()
        buffer.close()
        return zipdata

    def getSignedPass(self, wwdrcert, cert, key, passphrase = None):
        if not (self.type and self.description and self.organizationName, self.passTypeIdentifier, self.teamIdentifier and self.serialNumber and self.formatVersion):
            raise ValueError #values are required

        package = self.getPackage()
        manifest = package["manifest.json"]
        signature = self.sign(manifest, wwdrcert, cert, key, passphrase)
        package["signature"] = signature
        return self.zipPackage(package)
        
