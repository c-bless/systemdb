from flask import Blueprint

import_bp = Blueprint('importer', __name__, template_folder="templates", url_prefix='/importer')

from systemdb.webapp.importer.views import upload_post, upload, import_file_by_name, import_all