from push_utils import b2WorldInterface, make_base, create_body, end_effector, run_simulation
import sys
import numpy as np


class PushReward:
    def __init__(self, seed):

        # domain of this function
        self.xmin = [-5., -5., -10., -10., 2., 0., -5., -5., -10., -10., 2., 0., -5., -5.]
        self.xmax = [5., 5., 10., 10., 30., 2.*np.pi, 5., 5., 10., 10., 30., 2.*np.pi, 5., 5.]

        # starting xy locations for the two objects
        self.sxy = (0, 2)
        self.sxy2 = (0, -2)
        # goal xy locations for the two objects
        self.gxy = [4, 3.5]
        self.gxy2 = [-4, 3.5]
        
        #seed added for reproductibility
        self.seed=seed

    @property
    def f_max(self):
        # maximum value of this function
        return np.linalg.norm(np.array(self.gxy) - np.array(self.sxy)) \
            + np.linalg.norm(np.array(self.gxy2) - np.array(self.sxy2))
    @property
    def dx(self):
        # dimension of the input
        return self._dx
    
    def __call__(self, argv):
        # returns the reward of pushing two objects with two robots
        
        rx = float(argv[0])
        ry = float(argv[1])
        xvel = float(argv[2])
        yvel = float(argv[3])
        simu_steps = int(float(argv[4]) * 10)
        init_angle = float(argv[5])*np.pi
        rx2 = float(argv[6])
        ry2 = float(argv[7])
        xvel2 = float(argv[8])
        yvel2 = float(argv[9])
        simu_steps2 = int(float(argv[10]) * 10)
        init_angle2 = float(argv[11])*np.pi
        rtor = float(argv[12])
        rtor2 = float(argv[13])
        
        initial_dist = self.f_max
     
        world = b2WorldInterface(True)
        oshape, osize, ofriction, odensity, bfriction, hand_shape, hand_size = 'circle', 1, 0.01, 0.05, 0.01, 'rectangle', (1, 0.3)

        base = make_base(500, 500, world)
        body = create_body(base, world, 'rectangle', (0.5, 0.5), ofriction, odensity, self.sxy)
        body2 = create_body(base, world, 'circle', 1, ofriction, odensity, self.sxy2)

        robot = end_effector(world, (rx,ry), base, init_angle, hand_shape, hand_size)
        robot2 = end_effector(world, (rx2,ry2), base, init_angle2, hand_shape, hand_size)
        (ret1, ret2) = run_simulation(world, body, body2, robot, robot2, xvel, yvel, \
                                      xvel2, yvel2, rtor, rtor2, simu_steps, simu_steps2, self.seed)
        
        ret1 = np.linalg.norm(np.array(self.gxy) - ret1)
        ret2 = np.linalg.norm(np.array(self.gxy2) - ret2)
        return initial_dist - ret1 - ret2 


def push(x0,seed):
    
    if type(x0)==str :
        filename = x0
        #filename = sys.argv[1]
        file = open(filename, 'r')
        x = file.read().split()
        file.close()
    else :
        x=x0
    
    dim = len(x)
    for i in range(dim) :
        x[i] = float(x[i])
    
    f = PushReward(seed)
    #x = np.random.uniform(f.xmin, f.xmax)
    #print('Input = {}'.format(x))
    #print('Output = {}'.format(f(x)))
    res = f(x)
    
    print(res)