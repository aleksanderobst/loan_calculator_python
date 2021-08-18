import argparse
import math
import sys


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--type", help="Type of the operation: annuity or diff")

    parser.add_argument('-P', '--principal', help='The loan principal', type=int, dest="principal", required=False)
    parser.add_argument('-p', '--periods', help='The number of periods', type=int, dest="periods", required=False)
    parser.add_argument('-i', '--interest', help='The loan interest', type=float, dest="interest", required=False)
    parser.add_argument('-c', '--payment', help='The monthly payment', type=int, dest="payment", required=False)

    args = parser.parse_args()

    if args.type != "diff" and args.type != "annuity" or \
            args.type == "diff" and args.payment is not None or \
            args.type == "annuity" and args.interest is None or \
            args.type == "diff" and args.interest is None or \
            len(sys.argv) < 5 or \
            (args.principal is not None and args.principal < 0 or
             args.payment is not None and args.payment < 0 or
             args.periods is not None and args.periods < 0 or
             args.interest is not None and args.interest < 0):

        print("Incorrect parameters")
    elif args.type == 'diff':
        nominal_interest_rate = args.interest / (12 * 100)
        principal2 = args.principal

        for x in range(1, args.periods + 1):
            print("Month " + str(x) + ": payment is " + str(math.ceil(
                args.principal / args.periods + nominal_interest_rate * (
                        args.principal - (args.principal * (x - 1) / args.periods)))))

            principal2 -= math.ceil(args.principal / args.periods + nominal_interest_rate * (
                    args.principal - (args.principal * (x - 1) / args.periods)))
        print()
        print("Overpayment = " + str(abs(principal2)))

    elif args.type == 'annuity' and args.payment is None:
        nominal_interest_rate = args.interest / (12 * 100)

        monthly_payment = args.principal * (nominal_interest_rate * pow(1 + nominal_interest_rate, args.periods)) / \
        (pow(1 + nominal_interest_rate, args.periods) - 1)

        print("Your annuity payment = " + str(math.ceil(monthly_payment)) + "!")
        principal2 = (math.ceil(monthly_payment) * args.periods) - args.principal

        print("Overpayment = " + str(math.ceil(principal2)))

    elif args.type == 'annuity' and args.principal is None:
        nominal_interest_rate = args.interest / (12 * 100)

        principal = args.payment / ((nominal_interest_rate * pow(1 + nominal_interest_rate, args.periods)) /
                                    (pow(1 + nominal_interest_rate, args.periods) - 1))

        print("Your loan principal = " + str(math.floor(principal)) + "!")
        principal2 = (math.ceil(args.payment) * args.periods) - principal

        print("Overpayment = " + str(math.ceil(principal2)))

    elif args.type == 'annuity' and args.periods is None:
        nominal_interest_rate = args.interest / (12 * 100)

        number_of_months = math.ceil(
            math.log((args.payment / (args.payment - nominal_interest_rate * args.principal)),
                     1 + nominal_interest_rate))

        years = math.floor(number_of_months / 12)
        months = number_of_months - (years * 12)

        output_message = "It will take"
        if years:
            output_message += f" {years} year" if years == 1 else f" {years} years"
        if months and months != 12:
            output_message += f" and {months} month" if months == 1 else f" and {months} months"
        output_message += " to repay this loan!"

        print(output_message)
        principal2 = (math.ceil(args.payment) * number_of_months) - args.principal

        print("Overpayment = " + str(math.ceil(principal2)))

    else:
        print("Error:Requires an argument to perform an action")


if __name__ == '__main__':
    main()
