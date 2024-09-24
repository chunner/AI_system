import sys
import numpy as np
import struct
import os
import time

def show_matrix(mat, name):
    #print(name + str(mat.shape) + ' mean %f, std %f' % (mat.mean(), mat.std()))
    pass

def show_time(time, name):
    #print(name + str(time))
    pass


class FullyConnectedLayer(object):
    def __init__(self, num_input, num_output):  # 全连接层初始化
        self.num_input=num_input            # 输入的单元数
        self.num_output=num_output          # 输出的单元数
        print('\tFully connected layer with input %d, output %d.' % (self.num_input, self.num_output))
    def init_param(self, std=0.01):  # 参数初始化   std: 初始化权重的标准差，默认值为 0.01
        self.weight = np.random.normal(loc=0.0, scale=std, size=(self.num_input, self.num_output))      # 从正态分布中生成随机数，作为权重矩阵的初始值
        self.bias=np.zeros([1, self.num_output])            # 使用 np.zeros 初始化偏置为零，形状为 [1, self.num_output]
        show_matrix(self.weight, 'fc weight ')
        show_matrix(self.bias, 'fc bias ')
    def forward(self, input): # 前向传播计算
        start_time = time.time()
        self.input=input
        # TODO：全连接层的前向传播，计算输出结果
        # self.output= np.matmul(self.input, self.weight) + self.bias      # Y = XW + b^T
        self.output = np.zeros((self.input.shape[0], self.num_output))
        for n in range(self.input.shape[0]):
            self.output[n] = np.matmul(self.input[n], self.weight) + self.bias[0]
        
        input = np.random.rand(100000, 1000)  # m: 输入特征的数量
        weight = np.random.rand(1000, 100)     # p: 输出特征的数量
        bias = np.random.rand(1, 100)
        output = np.zeros((100000, 100))     # 输出矩阵

        for n in range(100000):
            output[n] = np.matmul(input[n], weight) + bias[0]

            
        return self.output

    def backward(self, top_diff):   # 反向传播的计算
        # TODO：全连接层的反向传播，计算参数梯度和本层损失
        self.d_weight=self.input.T @ top_diff
        self.d_bias= np.sum(top_diff.T, axis=1)# top_diff.T  @ np.ones((top_diff.shape[1],))
        bottom_diff= top_diff @ self.weight.T

        return bottom_diff
    def get_gradient(self):

        return self.d_weight,self.d_bias

    def update_param(self, lr):  # 参数更新         lr 学习率
        # TODO：对全连接层参数利用参数进行更新
        self.weight= self.weight - lr * self.d_weight
        self.bias= self.bias - lr * self.d_bias
        
    def load_param(self, weight, bias): # 参数加载
        assert self.weight.shape == weight.shape
        assert self.bias.shape == bias.shape
        self.weight=weight
        self.bias=bias
        show_matrix(self.weight, 'fc weight ')
        show_matrix(self.bias, 'fc bias ')

    def save_param(self):    # 参数保存
        show_matrix(self.weight, 'fc weight ')
        show_matrix(self.bias, 'fc bias ')
        return self.weight, self.bias


class ReLULayer(object):
    def __init__(self):
        print('\t Relu layer')

    def forward(self, input):  # 前向传播的计算
        start_time = time.time()
        self.input=input
        # TODO：ReLU层的前向传播，计算输出结果
        output=np.maximum(0, input)
        return output
    def backward(self, top_diff):   # 反向传播的计算
        # TODO：ReLU层的反向传播，计算本层损失
        bottom_diff=top_diff * (self.input > 0)
        return bottom_diff

class SoftmaxLossLayer(object):
    def __init__(self):
        print('\tSoftmax loss layer.')
    def forward(self, input):  # 前向传播的计算
        # TODO：softmax 损失层的前向传播，计算输出结果
        input_max = np.max(input, axis=1, keepdims=True)
        input_exp = np.exp(input-input_max)
        exp_sum = np.sum(input_exp, axis=1, keepdims=True)
        self.prob = input_exp / exp_sum
        return self.prob

    def get_loss(self,label):  # 计算损失
        self.batch_size=self.prob.shape[0]
        self.label_onehot=np.zeros_like(self.prob)
        self.label_onehot[np.arange(self.batch_size),label]=1.0
        loss=-np.sum(np.log(self.prob)*self.label_onehot)/self.batch_size
        return loss
    def backward(self):   # 反向传播的计算
        # TODO：softmax 损失层的反向传播，计算本层损失
        bottom_diff= (self.prob - self.label_onehot) /self.batch_size
        return bottom_diff



