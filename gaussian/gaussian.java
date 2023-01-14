import java.util.*;
import java.io.*;

public class gaussian
{
    // Foward Elimination

    public static void FwdElimination(double[][] a, double[] b)
    {
        int n = b.length;
        for (int k = 0; k < n-1; k++)
        {
            for (int i = k + 1; i < n; i++)
            {
                double mult = a[i][k] / a[k][k];
                for(int j = k; j < n; j++)
                {
                    a[i][j] = a[i][j] - mult * a[k][j];
                }
                b[i] = b[i] - mult * b[k];
            }
        }
    }
    
    // Back Substitution

    public static void BackSubst(double[][] a, double[] b, double[] sol)
    {
        int n = b.length-1;
        for (int i = n; i >= 0; i--)
        {
            double sum = b[i];
            for(int j = i+1; j < n; j++)
            {
                sum = sum - a[i][j] * sol[j];
            }
            sol[i] = sum / a[i][i];
        }
    }
    public static void main(String[] args) throws Exception {
    {
        try
        {
            File sys = new File("./sys1.lin");
            Scanner fileReader = new Scanner(sys);
            int n = fileReader.nextInt();
            int lineNum = 0;
            double[][] matrix = new double[n][n];
            double[] values = new double[n];

            while(fileReader.hasNextDouble())
            {
                if(lineNum < n)
                {
                    for(int i = 0; i < n; i++)
                    {
                        for(int j = 0; j < n; j++)
                        {
                            matrix[i][j] = fileReader.nextDouble();                
                        }
                        lineNum++;
                    }
                }
                else
                {
                    for(int i = 0; i < n; i++)
                    {
                        values[i] = fileReader.nextDouble();
                    }
                }

            }
            fileReader.close();

            double[] solutions = new double[n];
            FwdElimination(matrix, values);
            BackSubst(matrix, values, solutions);
            System.out.println(Arrays.toString(solutions));

           FileWriter Writer = new FileWriter("./sys1.sol");
           Writer.write(Arrays.toString(solutions));
           Writer.close();
        }
        catch(FileNotFoundException e)
        {
            System.out.print(e);

        }
    }
}
}