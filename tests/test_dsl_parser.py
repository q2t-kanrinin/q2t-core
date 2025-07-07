from parse_fold_dsl import DSLParser


def test_dsl_parser_comments():
    parser = DSLParser("docs/fold_dsl-sample.yaml")
    dsl = parser.parse()
    assert parser.meta_title == "Fold DSL Sample"
    assert parser.meta_tags == ["sample", "fold"]
    assert dsl.sections[0].id == "A-01"
    assert len(dsl.links) == 2
