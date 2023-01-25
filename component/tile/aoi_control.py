from sepal_ui import aoi
from sepal_ui.scripts import utils as su
from sepal_ui import color as sc
from sepal_ui import mapping as sm
import ee

from component import parameter as cp
from component.message import cm


class AoiView(aoi.AoiView):
    """
    Extend the aoi_view component from sepal_ui.mapping to add
    the extra coloring parameter used in this application. To do so we were
    forced to copy/paste the _update_aoi
    """

    def __init__(self, **kwargs):

        # create the map
        super().__init__(methods=["-POINTS"], **kwargs)

        # nest the tile
        self.elevation = False

        # change btn color
        self.btn.color = "secondary"

    @su.loading_button(debug=False)
    def _update_aoi(self, widget, event, data):
        """
        extention of the original method that display information on the map.
        In the ee display we changed the display parameters
        """

        # update the model
        self.model.set_object()

        # update the map
        [self.map_.remove_layer(lr) for lr in self.map_.layers if lr.name == "aoi"]
        self.map_.zoom_bounds(self.model.total_bounds())
        empty = ee.Image().byte()
        outline = empty.paint(featureCollection=self.model.feature_collection, color=1, width=2)
        self.map_.addLayer(outline, {"palette": sc.primary}, "aoi")
        self.map_.hide_dc()

        # tell the rest of the apps that the aoi have been updated
        self.updated += 1


class AoiControl(sm.MenuControl):
    def __init__(self, map_):

        # create the view
        self.view = AoiView(map_=map_)
        self.view.class_list.add("ma-5")

        # create the control
        super().__init__(
            "fa-solid fa-map-marker-alt", self.view, m=map_, card_title=cm.aoi_control.title
        )
