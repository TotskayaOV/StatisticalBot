from .update_data_wdb import update_wdb_portal
from .update_data_wdb import update_wdb_count_jira
from .update_data_wdb import update_wdb_sla_jira
from .update_data_wdb import update_wdb_time_jira
from .update_data_wdb import update_wdb_call
from .update_data_wdb import update_wdb_general
from .update_data_wdb import update_coordinator_evolutions

__all__ = ['update_wdb_portal', 'update_wdb_count_jira', 'update_wdb_sla_jira',
           'update_wdb_time_jira', 'update_wdb_call', 'update_wdb_general', 'update_coordinator_evolutions']