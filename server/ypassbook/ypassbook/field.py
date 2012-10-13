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
#2012/10/09


class Field:
    """
    An individul field for a Passbook in a pass.json
    """
    changeMessage = None
    label = None #localizable

    PKTEXT_ALIGNMENT_LEFT = "PKTextAlignmentLeft"
    PKTEXT_ALIGNMENT_CENTER = "PKTextAlignmentCenter"
    PKTEXT_ALIGNMENT_RIGHT = "PKTextAlignmentRight"
    PKTEXT_ALIGNMENT_NATURAL = "PKTextAlignmentNatural"

    textAlignment = None 

    PKDATE_STYLE_NONE = "PKDateStyleNone"
    PKDATE_STYLE_SHORT = "PKDateStyleShort"
    PKDATE_STYLE_MEDIUM = "PKDateStyleMedium"
    PKDATE_STYLE_LONG = "PKDateStyleLong"
    PKDATE_STYLE_FULL = "PKDateStyleFull"

    dateStyle = None

    timeStyle = None # specify both dateStyle and timeStyle, or neither
    isRelative = None

    currencyCode = None # ISO 4217 currency code for the field's value

    PKNUMBER_STYLE_DECIMAL = "PKNumberStyleDecimal"
    PKNUMBER_STYLE_PERCENT = "PKNumberStylePercent"
    PKNUMBER_STYLE_SCIENTIFIC = "PKNumberStyleScientific"
    PKNUMBER_STYLE_SPELLOUT = "PKNumberStyleSpellOut"

    numberStyle = None

    def __init__(self, key, value, label = None, dateStyle = None, timeStyle = None, isRelative = None, currencyCode = None, numberStyle = None):
        self.key = key

        #localizable, ISO 8601 date as a string, or number
        if dateStyle or timeStyle or isRelative:
            self.value = str(value)
            if (dateStyle and timeStyle) or (not dateStyle and not timeStyle):
                self.dateStyle = dateStyle
                self.timeStyle = timeStyle
            else:
                raise ValueError

            if isRelative:
                self.isRelative = isRelative
        elif currencyCode or numberStyle:
            self.value = value
            if currencyCode:
                self.currencyCode = currencyCode
            if numberStyle:
                self.numberStyle = numberStyle
        else:
            self.value = str(value)
        self.label = label
            
    def getDict(self):
        field = {}
        field["key"] = self.key
        field["value"] = self.value
        if self.changeMessage:
            field["changeMessage"] = self.changeMessage
        if self.label:
            field["label"] = self.label
        if self.textAlignment:
            field["textAlignment"] = self.textAlignment
        if self.dateStyle or self.timeStyle or self.isRelative:
            if self.dateStyle and self.timeStyle:
                field["dateStyle"] = self.dateStyle
                field["timeStyle"] = self.timeStyle
            if self.isRelative:
                field["isRelative"] = self.isRelative
        else:
            if self.currencyCode:
                field["currencyCode"] = self.currencyCode
            if self.numberStyle:
                field["numberStyle"] = self.numberStyle
        return field

    def __repr__(self):
        return repr(self.getDict())
