<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="0" simplifyDrawingHints="0" simplifyAlgorithm="0" styleCategories="AllStyleCategories" version="3.8.0-Zanzibar" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyMaxScale="1" simplifyLocal="1" maxScale="0" readOnly="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" forceraster="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol name="0" type="marker" clip_to_extent="1" alpha="1" force_rhr="0">
        <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
          <prop k="angle" v="0"/>
          <prop k="color" v="135,126,227,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="star"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="7.5"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" name="name" type="QString"/>
              <Option name="properties"/>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory lineSizeType="MM" barWidth="5" diagramOrientation="Up" penWidth="0" sizeScale="3x:0,0,0,0,0,0" lineSizeScale="3x:0,0,0,0,0,0" opacity="1" rotationOffset="0" penAlpha="255" scaleDependency="Area" width="15" backgroundColor="#ffffff" minimumSize="0" maxScaleDenominator="1e+08" minScaleDenominator="0" scaleBasedVisibility="0" sizeType="MM" backgroundAlpha="255" penColor="#000000" enabled="0" height="15" labelPlacementMethod="XHeight">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute color="#000000" field="" label=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings dist="0" zIndex="0" obstacle="0" priority="0" showAll="1" placement="0" linePlacementFlags="2">
    <properties>
      <Option type="Map">
        <Option value="" name="name" type="QString"/>
        <Option name="properties" type="Map">
          <Option name="positionX" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
          <Option name="positionY" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
          <Option name="show" type="Map">
            <Option value="true" name="active" type="bool"/>
            <Option value="ID" name="field" type="QString"/>
            <Option value="2" name="type" type="int"/>
          </Option>
        </Option>
        <Option value="collection" name="type" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="ID">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="Elevation">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="InitLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MinLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MaxLevel">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Diameter">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="MinVolume">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="VolumeCurv">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Desc">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ID" name="" index="0"/>
    <alias field="Elevation" name="" index="1"/>
    <alias field="InitLevel" name="" index="2"/>
    <alias field="MinLevel" name="" index="3"/>
    <alias field="MaxLevel" name="" index="4"/>
    <alias field="Diameter" name="" index="5"/>
    <alias field="MinVolume" name="" index="6"/>
    <alias field="VolumeCurv" name="" index="7"/>
    <alias field="Desc" name="" index="8"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="ID" expression="" applyOnUpdate="0"/>
    <default field="Elevation" expression="0" applyOnUpdate="0"/>
    <default field="InitLevel" expression="10" applyOnUpdate="0"/>
    <default field="MinLevel" expression="0" applyOnUpdate="0"/>
    <default field="MaxLevel" expression="20" applyOnUpdate="0"/>
    <default field="Diameter" expression="50" applyOnUpdate="0"/>
    <default field="MinVolume" expression="0" applyOnUpdate="0"/>
    <default field="VolumeCurv" expression="''" applyOnUpdate="0"/>
    <default field="Desc" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="ID" notnull_strength="2" constraints="1" unique_strength="0"/>
    <constraint exp_strength="0" field="Elevation" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="InitLevel" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="MinLevel" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="MaxLevel" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="Diameter" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="MinVolume" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="VolumeCurv" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="Desc" notnull_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ID" desc="" exp=""/>
    <constraint field="Elevation" desc="" exp=""/>
    <constraint field="InitLevel" desc="" exp=""/>
    <constraint field="MinLevel" desc="" exp=""/>
    <constraint field="MaxLevel" desc="" exp=""/>
    <constraint field="Diameter" desc="" exp=""/>
    <constraint field="MinVolume" desc="" exp=""/>
    <constraint field="VolumeCurv" desc="" exp=""/>
    <constraint field="Desc" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{feb3d7ef-ebdd-49b9-84c6-58eeac6951f6}" key="Canvas"/>
    <actionsetting notificationMessage="" action="" name="" isEnabledOnlyWhenEditable="0" type="0" capture="0" icon="" id="{68f0c7a1-8fc4-4c7f-925b-651c56f1c8f0}" shortTitle="">
      <actionScope id="Canvas"/>
      <actionScope id="Field"/>
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" sortOrder="0" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="0" name="ID" type="field"/>
      <column width="-1" hidden="0" name="Elevation" type="field"/>
      <column width="-1" hidden="0" name="InitLevel" type="field"/>
      <column width="-1" hidden="0" name="MinLevel" type="field"/>
      <column width="-1" hidden="0" name="MaxLevel" type="field"/>
      <column width="-1" hidden="0" name="Diameter" type="field"/>
      <column width="-1" hidden="0" name="MinVolume" type="field"/>
      <column width="-1" hidden="0" name="VolumeCurv" type="field"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" hidden="0" name="Desc" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1">.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="Desc"/>
    <field editable="1" name="Diameter"/>
    <field editable="1" name="Elevation"/>
    <field editable="1" name="ID"/>
    <field editable="1" name="InitLevel"/>
    <field editable="1" name="MaxLevel"/>
    <field editable="1" name="MinLevel"/>
    <field editable="1" name="MinVolume"/>
    <field editable="1" name="VolumeCurv"/>
  </editable>
  <labelOnTop>
    <field name="Desc" labelOnTop="0"/>
    <field name="Diameter" labelOnTop="0"/>
    <field name="Elevation" labelOnTop="0"/>
    <field name="ID" labelOnTop="0"/>
    <field name="InitLevel" labelOnTop="0"/>
    <field name="MaxLevel" labelOnTop="0"/>
    <field name="MinLevel" labelOnTop="0"/>
    <field name="MinVolume" labelOnTop="0"/>
    <field name="VolumeCurv" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>ID</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
