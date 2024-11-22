from inspyollama_client.helpers import filesystem


if hasattr(filesystem, 'file_has_recall_attribute'):
    from inspyollama_client.helpers.filesystem import file_has_recall_attribute
