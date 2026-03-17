from flask import Blueprint, request, jsonify
from Controllers import FoldersController

folder_bp = Blueprint('folder_bp', __name__)
@folder_bp.route('/folders', methods=['POST'])
def create_folder():
    data = request.get_json()
    result = FoldersController.create_folder(data)
    return jsonify(result), result['status']

@folder_bp.route('/folders/list', methods=['GET'])
def get_all_folders():
   return FoldersController.get_all_folders()
   
@folder_bp.route('/folders/number/archive', methods=['GET'])
def get_all_folders_number_archive():
   return FoldersController.get_number_folder_archive()
   
@folder_bp.route('/folders/number/noarchive', methods=['GET'])
def get_all_folders_number_not_archive():
   return FoldersController.get_number_folder_not_archive()
       
@folder_bp.route('/folders/archive', methods=['GET'])
def get_all_folders_archive():
   return FoldersController.get_all_folders_archive()
   
@folder_bp.route('/folders/<int:folder_id>', methods=['GET'])
def get_folder_by_id(folder_id):
    return FoldersController.get_folder_by_id(folder_id)
    
@folder_bp.route('/folders/number', methods=['GET'])
def get_folder_number():
    return FoldersController.get_number_folder()

@folder_bp.route('/folders/<int:folder_id>', methods=['PUT'])
def update_folder(folder_id):
    data = request.get_json()
    result = FoldersController.update_folder(folder_id, data)
    return jsonify(result), result['status']
    
@folder_bp.route('/folders/<int:folder_id>', methods=['PATCH'])
def archive_folder(folder_id):
    result = FoldersController.archive_folder(folder_id)
    return jsonify(result), result['status']
    
@folder_bp.route('/folders/no/<int:folder_id>', methods=['PATCH'])
def no_archive_folder(folder_id):
    result = FoldersController.no_archive_folder(folder_id)
    return jsonify(result), result['status']
    
@folder_bp.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    return FoldersController.delete_folder(folder_id)
    
@folder_bp.route('/folders/list', methods=['GET'])
def folder_per_month():
    return FoldersController.get_number_folder_per_month()
