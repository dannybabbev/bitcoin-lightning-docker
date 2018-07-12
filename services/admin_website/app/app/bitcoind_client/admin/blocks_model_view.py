from flask import flash
from flask_admin.model import BaseModelView

from app.bitcoind_client.bitcoind_client import BitcoinClient
from app.bitcoind_client.forms import MineBlocksForm
from app.bitcoind_client.models.blocks import Blocks


class BlocksModelView(BaseModelView):
    bitcoin = BitcoinClient()
    can_view_details = True

    def get_pk_value(self, model):
        return model.hash

    def scaffold_list_columns(self):
        return ['hash', 'confirmations', 'strippedsize', 'size', 'weight',
                'height', 'version', 'versionHex', 'merkleroot', 'tx', 'time',
                'mediantime', 'nonce', 'bits', 'difficulty', 'chainwork', 'nTx']

    def scaffold_sortable_columns(self):
        pass

    def scaffold_form(self):
        return MineBlocksForm

    def scaffold_list_form(self, widget=None, validators=None):
        pass

    def get_list(self, page, sort_field, sort_desc, search, filters,
                 page_size=None):
        blocks = self.bitcoin.get_most_recent_blocks()
        blocks = [Blocks(**b) for b in blocks]
        return self.bitcoin.get_block_count(), blocks

    def get_one(self, block_hash):
        block = self.bitcoin.get_block(block_hash=block_hash, verbosity=2)
        return Blocks(**block)

    def create_model(self, form):
        num_blocks_to_mine = form.num_blocks.data
        message, category = self.bitcoin.generate(num_blocks_to_mine=num_blocks_to_mine)
        flash(message=message, category=category)
        return Blocks()

    def update_model(self, form, model):
        pass

    def delete_model(self, model):
        pass
