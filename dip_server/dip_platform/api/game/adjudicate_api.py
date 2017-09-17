from dip_platform.api.generic_view import GenericView
from dip_platform.logic.game.resolution import resolution_logic


class AdjudicateView(GenericView):
    def handle_put(self, request, data):
        payload = resolution_logic.resolve_turn(data)

        status = 200
        headers = dict()
        return status, payload, headers
