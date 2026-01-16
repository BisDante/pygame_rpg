<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.2" name="placeholder" tilewidth="32" tileheight="32" tilecount="6" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="traversable">
  <image source="../../images/tiles/brick2.png" width="32" height="32"/>
 </tile>
 <tile id="1" type="non_traversable">
  <image source="../../images/tiles/brick.png" width="32" height="32"/>
 </tile>
 <tile id="2" type="door">
  <properties>
   <property name="contains" value=""/>
  </properties>
  <image source="../../images/tiles/door.png" width="32" height="32"/>
 </tile>
 <tile id="3" type="player">
  <image source="../../images/actors/player.png" width="32" height="32"/>
 </tile>
 <tile id="4" type="enemy">
  <properties>
   <property name="contains" value=""/>
  </properties>
  <image source="../../images/actors/enemy.png" width="32" height="32"/>
 </tile>
 <tile id="5" type="treasure">
  <properties>
   <property name="contains" value=""/>
  </properties>
  <image source="../../images/objects/treasure.png" width="32" height="32"/>
 </tile>
</tileset>
