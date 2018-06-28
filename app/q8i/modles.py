import datetime, json, inspect

from tables import db, STAT, Community, MyHouse, Monitor


def comny_add(comnyID, comnyName, st=STAT.OPEN):
    ''' 添加小区 '''
    comny = Community()
    comny.id = comnyID
    comny.community = comnyName
    comny.status = st
    db.session.add(comny)
    db.session.commit()

def house_add(phone, comnyID, comnyName, site, st=STAT.OPEN):
    ''' 添加住宅信息 '''
    house = MyHouse()
    house.phone = phone
    house.community = comnyName
    house.communityID = comnyID
    house.site = site
    house.sip = comnyID + site
    house.status = st
    db.session.add(house)
    db.session.commit()

def house_del(phone, comnyID, site):
    ''' 删除住宅信息 '''
    house = MyHouse.query.filter(phone == MyHouse.phone, comnyID == MyHouse.communityID, site == MyHouse.site).first()
    if house is None:
        return 
    db.session.delete(house)
    db.session.commit()
