---
layout: post
cover: 'assets/images/crazy.png'
title: Java Simple Calculator
date: 2020-11-18 12:00:00
tags: java swing
author: sjh
---



<p>
    swing ui 编写、功能简单且存在一点瑕疵的计算器程序
</p>

# 简易计算器

#### 程序解释

###### 原理详解

从类的设计的角度上来讲，计算器应该是界面与操作分离，由界面程序获取操作数并传递给计算程序，从计算程序中获取结果。

###### 类的设计

1. Calculator

   用于计算的类，传入操作数和操作符后可获取结果，运算错误抛出异常。

2. Calculator Frame

   计算器的界面类，提供操作数和操作符。

###### 结构解析

	Calculator类采用两个堆栈分别存放运算数和操作符，在计算时从中抛出操作数与操作符。对小数和负数，采用标记位进行判断。

小数：当输入了小数点“.“后，记录接下来输入数字的个数，在数字输入结束后（即输入操作符）时，将栈中的第一位数抛出并转化为小数

负数：当输入了”neg"标记后，同上，在同一时刻转化成负数

输入数字或者操作符后，自动检查堆栈元素进行计算，因此这个简易计算器在按下“=”前，在特定情况下，会先计算部分算式；

~~*另一种思路：输入的任何符号都先记录起来等按下“=”时再进行读取数字和操作符进行运算*~~

###### 缺点

	因为即时运算的原因，计算器无法实现单步删除功能，只能直接清空重置计算器。代码可拓展性差，添加新的操作符运算可能需要改动部分原有逻辑。

~~要不要改？卧槽，我懒啊！~~

#### 源码展示

###### Calculator.java

```java
package calculator;

import com.sun.xml.internal.ws.api.ha.StickyFeature;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

public class Calculator {
    private final HashMap<String, Integer> operatorPriority;

    private final LinkedList<Double> numberStack;
    private final LinkedList<String> operatorStack;

    /**
     * 是否开始输入下一个数字
     */
    private boolean nextNum;
    /**
     * 是否已经完成了一次计算
     */
    private boolean calculated;
    /**
     * 是否输入了小数
     */
    private boolean decimal;
    private int decimalDigits;
    /**
     * 是否输入了负数
     */
    private boolean negative;

    public Calculator() {
        operatorPriority = new HashMap<>();
        numberStack = new LinkedList<>();
        operatorStack = new LinkedList<>();

        List<String> level1 = Arrays.asList("+", "-");
        List<String> level2 = Arrays.asList("*", "/", "%");
        level1.forEach(op -> operatorPriority.put(op, 1));
        level2.forEach(op -> operatorPriority.put(op, 2));


        reset();
    }

    public void reset() {
        calculated = true;
        numberStack.clear();
        operatorStack.clear();
        numberStack.push(0.0);
        nextNum = true;
        negative = false;
        decimal = false;
        decimalDigits = 0;
    }

    /**
     * 是否已经完成了一次计算
     */
    public boolean isCalculated() {
        return this.calculated;
    }

    /**
     * 获得计算结果
     *
     * @return 计算结果
     * @throws ArithmeticException 如果输入不合法运算公式则抛出这个异常
     */
    public double getResult() throws ArithmeticException {
        tryDecimal();
        tryNegative();

        while (!numberStack.isEmpty() && !operatorStack.isEmpty()) {
            double num2 = numberStack.pop();
            double num1 = numberStack.pop();
            String operator = operatorStack.pop();
            numberStack.push(calculate(num1, num2, operator));
        }

        calculated = true;

        if (numberStack.isEmpty()) {
            return 0.0;
        } else {
            return numberStack.peek();
        }
    }

    /**
     * 输入一个操作数
     *
     * @param value 整数
     */
    public void inputNum(int value) {
        double number = value;
        if (!nextNum) {
            number = numberStack.pop();
            number = number * 10 + value;
            if (decimal) decimalDigits++;
        }
        numberStack.push(number);

        //开始输入当前这个数字
        nextNum = false;
        //还未完成一次计算
        calculated = false;
    }

    /**
     * 输入一个运算符号
     *
     * @param op 运算符号，目前仅支持“+、-、*、/“，支持小数和负数
     * @throws ArithmeticException 如果输入不合法运算公式则抛出这个异常
     */
    public void inputOperator(String op) throws ArithmeticException {
        //输入运算符时意味着正在进行运算（即未完成）
        calculated = false;

        if (op.equals(".")) {
            decimal = true;
            return;
        }

        if(op.equals("neg")){
            negative = !negative;
            return;
        }

        tryDecimal();
        tryNegative();

        while (!operatorStack.isEmpty() && compareOperator(op, operatorStack.peek()) < 0) {
            Double num2 = numberStack.pop();
            Double num1 = numberStack.pop();
            String operator = operatorStack.pop();
            numberStack.push(calculate(num1, num2, operator));
        }

        operatorStack.push(op);

        //输运算符后意味着开始输入下一个数字
        nextNum = true;
    }

    /**
     * 检验是否输入了小数
     */
    private boolean tryDecimal() {
        //如果刚刚输入的数字（即栈顶）是小数
        if (decimal) {
            double top = numberStack.pop();
            top *= Math.pow(10, -1 * decimalDigits);
            numberStack.push(top);

            //下一个数字不一定是小数，重置小数参数
            decimal = false;
            decimalDigits = 0;

            return true;
        }
        return false;
    }

    private boolean tryNegative() {
        if(negative){
            double top = numberStack.pop();
            numberStack.push(-top);

            //重置标记
            negative = false;

            return true;
        }
        return false;
    }

    private double calculate(double num1, double num2, String op) {
        //使用string类型消除double精度误差
        BigDecimal bigNum1 = new BigDecimal(String.valueOf(num1));
        BigDecimal bigNum2 = new BigDecimal(String.valueOf(num2));
        BigDecimal result;
        switch (op) {
            case "+":
                result = bigNum1.add(bigNum2);
                break;
            case "-":
                result = bigNum1.subtract(bigNum2);
                break;
            case "*":
                result = bigNum1.multiply(bigNum2);
                break;
            case "/":
                result = bigNum1.divide(bigNum2, BigDecimal.ROUND_HALF_UP);
                break;
            default:
                throw new ArithmeticException();
        }

        return result.doubleValue();
    }

    private int compareOperator(String op1, String op2) {
        int op1Level = 0, op2Level = 0;

        op1Level = operatorPriority.get(op1);
        op2Level = operatorPriority.get(op2);

        return op1Level - op2Level;
    }

}
```



###### CalculatorFrame.java

```java
package calculator;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalculatorFrame extends JFrame {
    //region -JComponents-
    private JPanel northPanel;
    private JPanel centerPanel;
    private JPanel numberPanel;
    private JPanel operatorPanel;
    private JPanel southPanel;
    private JPanel westPanel;
    private JPanel eastPanel;
    private JTextField textArea;
    private JButton[] numberBtn;
    private JButton[] operatorBtn;
    private JButton point;
    private JButton delete;
    private JButton neg;
    //endregion

    private Calculator calculator;

    private void initComponent() {
        this.setLayout(new BorderLayout(10, 10));

        centerPanel = new JPanel(new BorderLayout(10, 6));
        numberPanel = new JPanel(new GridLayout(4, 4, 10, 10));
        operatorPanel = new JPanel(new GridLayout(6, 1, 10, 6));

        northPanel = new JPanel();
        southPanel = new JPanel();
        eastPanel = new JPanel();
        westPanel = new JPanel();

        textArea = new JTextField("0", 1);

        numberBtn = new JButton[10];
        operatorBtn = new JButton[5];
        delete = new JButton("AC");
        point = new JButton(".");
        neg = new JButton("neg");

        textArea.setEditable(false);
        textArea.setFont(new Font("微软雅黑", Font.BOLD, 24));
        textArea.setHorizontalAlignment(SwingConstants.TRAILING);

        point.setFont(new Font("黑体", Font.BOLD, 18));
        delete.setFont(new Font("黑体", Font.BOLD, 15));

        delete.addActionListener(event -> {
            textArea.setText("0");
            calculator.reset();
        });
        point.addActionListener(new OperatorButtonListener("."));
        neg.addActionListener(new OperatorButtonListener("neg"));

        for (int i = 0; i < 10; i++) {
            numberBtn[i] = new JButton(String.valueOf(i));
            numberBtn[i].addActionListener(new NumberButtonListener(i));
            numberBtn[i].setFont(new Font("黑体", Font.BOLD, 18));
            numberPanel.add(numberBtn[i]);
        }

        numberPanel.add(point);
        numberPanel.add(delete);

        operatorPanel.add(neg);

        String[] temp = {"+", "-", "*", "/", "="};
        for (int i = 0; i < operatorBtn.length; i++) {
            operatorBtn[i] = new JButton(temp[i]);
            operatorBtn[i].setFont(new Font("黑体", Font.BOLD, 18));
            operatorBtn[i].addActionListener(new OperatorButtonListener(temp[i]));
            operatorPanel.add(operatorBtn[i]);
        }


        centerPanel.add(BorderLayout.NORTH, textArea);
        centerPanel.add(BorderLayout.CENTER, numberPanel);
        centerPanel.add(BorderLayout.EAST, operatorPanel);

        this.add(BorderLayout.NORTH, northPanel);
        this.add(BorderLayout.CENTER, centerPanel);
        this.add(BorderLayout.SOUTH, southPanel);
        this.add(BorderLayout.EAST, eastPanel);
        this.add(BorderLayout.WEST, westPanel);

        this.pack();
        this.setSize(300, 300);
    }

    public CalculatorFrame() {
        initComponent();

        this.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        this.setLocationRelativeTo(null);
        this.setVisible(true);
        this.setTitle("简易计算器");

        calculator = new Calculator();
    }

    private class NumberButtonListener implements ActionListener {
        private final int value;

        public NumberButtonListener(int value) {
            this.value = value;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            if (calculator.isCalculated()) {
                calculator.reset();
                textArea.setText(String.valueOf(value));
            } else {
                textArea.setText(textArea.getText() + value);
            }

            calculator.inputNum(value);
        }
    }

    private class OperatorButtonListener implements ActionListener {
        private final String value;

        public OperatorButtonListener(String value) {
            this.value = value;
        }

        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                if (value.equals("=")) {
                    textArea.setText(String.valueOf(calculator.getResult()));
                } else {
                    if (value.equals("neg") && calculator.isCalculated()) {
                        textArea.setText(“neg”);
                    } else {
                        textArea.setText(textArea.getText() + value);
                    }
                    calculator.inputOperator(value);
                }
            } catch (ArithmeticException arithmeticException) {
                calculator.reset();
                textArea.setText("Error Input");
            }
        }
    }

    public static void main(String[] args) {
        new CalculatorFrame();
    }
}

```