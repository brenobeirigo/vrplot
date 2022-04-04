import vrplot.opt.complexity as comp


def test_solution_space():
    
    assert {
        ((0, 2, 3, 1, 0),),
        ((0, 3, 2, 1, 0),),
        ((0, 1, 3, 2, 0),),
        ((0, 3, 1, 2, 0),),
        ((0, 1, 2, 3, 0),),
        ((0, 2, 1, 3, 0),)
    } == comp.get_solution_space([1,2,3])
    
    assert {
        ((0, 0), (0, 0), (0, 1, 0)),
        ((0, 0), (0, 1, 0), (0, 0)),
        ((0, 1, 0), (0, 0), (0, 0))
    } == comp.get_solution_space([1], n_vehicles=3)
    
    assert {
        ((0, 0),
        (0, 0),
        (0, 1, 0))
    } == comp.get_solution_space([1], n_vehicles=3, distinguish_vehicles=False)