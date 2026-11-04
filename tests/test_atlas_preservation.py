import copy,unittest
from atlas_preservation import compare_section,graph_issues
class PreservationTests(unittest.TestCase):
 def setUp(self):self.rows=[{'id':'D-001','body':'A full original passage.','tags':['field'],'source':{'url':'https://example.org/source'}}]
 def test_addition_preserves_previous_record(self):self.assertEqual(compare_section(self.rows,self.rows+[{'id':'D-002','body':'A new passage.'}],'cards'),[])
 def test_missing_id_fails(self):self.assertTrue(compare_section(self.rows,[],'cards'))
 def test_truncated_body_fails(self):
  new=copy.deepcopy(self.rows);new[0]['body']='A full';self.assertTrue(compare_section(self.rows,new,'cards'))
 def test_deleted_source_fails(self):
  new=copy.deepcopy(self.rows);del new[0]['source'];self.assertTrue(compare_section(self.rows,new,'cards'))
 def test_removed_tag_fails(self):
  new=copy.deepcopy(self.rows);new[0]['tags']=[];self.assertTrue(compare_section(self.rows,new,'cards'))
 def test_expanded_body_preserves_original(self):
  new=copy.deepcopy(self.rows);new[0]['body']+=' Additional explanation.';self.assertEqual(compare_section(self.rows,new,'cards'),[])
 def test_reweighting_is_separate_from_substrate(self):
  old=copy.deepcopy(self.rows);old[0]['tagWeights']={'field':1};new=copy.deepcopy(old);new[0]['tagWeights']={'field':.6,'other':.4};self.assertEqual(compare_section(old,new,'cards'),[])
 def test_dangling_edge_fails(self):self.assertTrue(graph_issues({'nodes':[{'id':'D-001'}],'edgeFields':['id','from','to'],'edges':[['e','D-001','missing']]}))
 def test_changed_edge_endpoint_fails(self):self.assertTrue(compare_section([['e','A','B']],[['e','A','C']],'edges'))
 def test_swapped_edge_direction_fails(self):self.assertTrue(compare_section([['e','A','B']],[['e','B','A']],'edges'))
 def test_duplicate_id_fails(self):self.assertTrue(graph_issues({'nodes':[{'id':'A'},{'id':'A'}],'edgeFields':['id','from','to'],'edges':[]}))
if __name__=='__main__':unittest.main()
