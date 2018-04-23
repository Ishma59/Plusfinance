from decimal import Decimal as D
from dateutil.relativedelta import relativedelta
from micro_admin.calculators import ProfitsLossCalculator
from micro_admin.intervals import TimeInterval
from micro_admin.models import Receipts, Payments

class BaseReport(object):
    title = None
    period = None

    def __init__(self, title, start, end):
        self.title = title
        self.period = TimeInterval(start, end)

    def generate(self):
        raise NotImplementedError


class ProfitAndLossSummary(object):
    grouping_date = None
    income_amount = D('0')
    expenses_amount = D('0')
    expenses_dict = {
        "paymentofsalary_sum": sum([i.total_amount for i in paymentofsalary_list]),
        "printingcharges_sum": sum([i.total_amount for i in printingcharges_list]),
        "stationarycharges_sum": sum([i.total_amount for i in stationarycharges_list]),
        "travellingallowance_sum": sum([i.total_amount for i in travellingallowance_list]),
        "othercharges_sum": sum([i.total_amount for i in othercharges_list]),
    }
    #total expenses
    expenses_amount = sum([value for value in expenses_dict.values()])
      #income
    income_dict = {
        "total_loaninterest_amount_sum": sum([i["loaninterest_amount_sum"] for i in loaninterest_amount_sum_list]),
        "total_entrancefee_amount_sum": sum([i["entrancefee_amount_sum"] for i in entrancefee_amount_sum_list]),
        "total_membershipfee_amount_sum": sum([i["membershipfee_amount_sum"] for i in membershipfee_amount_sum_list]),
        "total_bookfee_amount_sum": sum([i["bookfee_amount_sum"] for i in bookfee_amount_sum_list]),
        "total_loanprocessingfee_amount_sum": sum([i["loanprocessingfee_amount_sum"] for i in loanprocessingfee_amount_sum_list]),

    }

    #Total income
    income_amount = sum([value for value in income_dict.values()])


    @property
    def net_profit(self):
        return self.income_amount - self.expenses_amount


class ProfitAndLossReport(BaseReport):
    # TODO implement 'Billed (Accrual) / Collected (Cash based)'
    organization = None
    summaries = None
    total_summary = None

    RESOLUTION_MONTHLY = 'monthly'
    RESOLUTION_CHOICES = (
        RESOLUTION_MONTHLY,
    )
    group_by_resolution = RESOLUTION_MONTHLY

    def __init__(self, organization, start, end):
        super().__init__("Profit and Loss", start, end)
        self.organization = organization
        self.summaries = {}
        steps_interval = relativedelta(end, start)

        assert self.group_by_resolution in self.RESOLUTION_CHOICES, \
            "No a resolution choice"
        if self.group_by_resolution == self.RESOLUTION_MONTHLY:
            for step in range(0, steps_interval.months):
                key_date = start + relativedelta(months=step)
                self.summaries[key_date] = ProfitAndLossSummary()
        else:
            raise ValueError("Unsupported resolution {}"
                .format(self.group_by_resolution))

        self.total_summary = ProfitAndLossSummary()

    def group_by_date(self, date):
        if self.group_by_resolution == self.RESOLUTION_MONTHLY:
            grouping_date = date.replace(day=1)
        else:
            raise ValueError("Unsupported resolution {}"
                .format(self.group_by_resolution))
        return grouping_date

    def generate(self):
        invoice_queryset = Invoice.objects.all()
        bill_queryset = Bill.objects.all()
        self.generate_for_income(invoice_queryset)
        self.generate_for_income(bill_queryset)

        # order the results
        self.summaries = OrderedDict(sorted(self.summaries.items()))

        # compute totals
        for summary in self.summaries.values():
            self.total_summary.income_amount += summary.income_amount
            self.total_summary.expenses_amount += summary.expenses_amount

    def generate_for_income(self, income_queryset):
        calculator = ProfitsLossCalculator(self.organization,
                                           start=self.period.start,
                                           end=self.period.end)

        for output in calculator.process_generator(income_queryset):
            key_date = self.group_by_date(output.payment.date_paid)
            summary = self.summaries[key_date]

            if isinstance(output.sale, Invoice):
                summary.income_amount += output.amount_excl_tax
            elif isinstance(output.sale, Bill):
                summary.expenses_amount += output.amount_excl_tax
            else:
                raise ValueError("Unsupported type of sale {}"
                    .format(output.sale.__class__))

