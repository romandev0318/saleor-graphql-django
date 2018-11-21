import { withStyles, WithStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import * as React from "react";

import { CardMenu } from "../../../components/CardMenu/CardMenu";
import { Container } from "../../../components/Container";
import DateFormatter from "../../../components/DateFormatter";
import PageHeader from "../../../components/PageHeader";
import SaveButtonBar from "../../../components/SaveButtonBar";
import Skeleton from "../../../components/Skeleton";
import i18n from "../../../i18n";
import { maybe } from "../../../misc";
import { UserError } from "../../../types";
import { DraftOrderInput } from "../../../types/globalTypes";
import { OrderDetails_order } from "../../types/OrderDetails";
import { UserSearch_customers_edges_node } from "../../types/UserSearch";
import OrderCustomer from "../OrderCustomer";
import OrderDraftDetails from "../OrderDraftDetails/OrderDraftDetails";
import { FormData as OrderDraftDetailsProductsFormData } from "../OrderDraftDetailsProducts";
import OrderHistory, { FormData as HistoryFormData } from "../OrderHistory";
import OrderProductAddDialog, {
  FormData as ProductAddFormData
} from "../OrderProductAddDialog";
import OrderShippingMethodEditDialog, {
  FormData as ShippingMethodForm
} from "../OrderShippingMethodEditDialog";

export interface OrderDraftPageProps {
  disabled: boolean;
  order: OrderDetails_order;
  users: UserSearch_customers_edges_node[];
  usersLoading: boolean;
  countries: Array<{
    code: string;
    label: string;
  }>;
  variants: Array<{
    id: string;
    name: string;
    sku: string;
    stockQuantity: number;
  }>;
  variantsLoading: boolean;
  errors: UserError[];
  fetchVariants: (value: string) => void;
  fetchUsers: (query: string) => void;
  onBack: () => void;
  onBillingAddressEdit: () => void;
  onCustomerEdit: (data: DraftOrderInput) => void;
  onDraftFinalize: () => void;
  onDraftRemove: () => void;
  onNoteAdd: (data: HistoryFormData) => void;
  onOrderLineAdd: () => void;
  onOrderLineChange: (
    id: string,
    data: OrderDraftDetailsProductsFormData
  ) => void;
  onOrderLineRemove: (id: string) => void;
  onProductClick: (id: string) => void;
  onShippingAddressEdit: () => void;
  onShippingMethodEdit: () => void;
}
interface OrderDraftPageState {
  openedBillingAddressEditDialog: boolean;
  openedDraftRemoveDialog: boolean;
  openedDraftFinalizeDialog: boolean;
  openedOrderLineAddDialog: boolean;
  openedShippingAddressEditDialog: boolean;
  openedShippingMethodEditDialog: boolean;
}

const decorate = withStyles(theme => ({
  date: {
    marginBottom: theme.spacing.unit * 3,
    marginLeft: theme.spacing.unit * 7
  },
  header: {
    marginBottom: 0
  },
  menu: {
    marginRight: -theme.spacing.unit
  },
  root: {
    display: "grid",
    gridColumnGap: theme.spacing.unit * 2 + "px",
    gridTemplateColumns: "9fr 4fr"
  }
}));
class OrderDraftPageComponent extends React.Component<
  OrderDraftPageProps & WithStyles<"date" | "header" | "menu" | "root">,
  OrderDraftPageState
> {
  state = {
    openedBillingAddressEditDialog: false,
    openedDraftFinalizeDialog: false,
    openedDraftRemoveDialog: false,
    openedOrderLineAddDialog: false,
    openedShippingAddressEditDialog: false,
    openedShippingMethodEditDialog: false
  };

  toggleDraftRemoveDialog = () =>
    this.setState(prevState => ({
      openedDraftRemoveDialog: !prevState.openedDraftRemoveDialog
    }));
  toggleDraftFinalizeDialog = () =>
    this.setState(prevState => ({
      openedDraftFinalizeDialog: !prevState.openedDraftFinalizeDialog
    }));
  toggleOrderLineAddDialog = () =>
    this.setState(prevState => ({
      openedOrderLineAddDialog: !prevState.openedOrderLineAddDialog
    }));
  toggleShippingMethodEditDialog = () =>
    this.setState(prevState => ({
      openedShippingMethodEditDialog: !prevState.openedShippingMethodEditDialog
    }));

  render() {
    const {
      classes,
      countries,
      disabled,
      errors,
      order,
      users,
      usersLoading,
      variants,
      variantsLoading,
      fetchUsers,
      fetchVariants,
      onBack,
      onBillingAddressEdit,
      onCustomerEdit,
      onDraftRemove,
      onDraftFinalize,
      onNoteAdd,
      onOrderLineAdd,
      onOrderLineChange,
      onOrderLineRemove,
      onShippingAddressEdit,
      onShippingMethodEdit
    } = this.props;
    const {
      openedBillingAddressEditDialog,
      openedDraftFinalizeDialog,
      openedDraftRemoveDialog,
      openedOrderLineAddDialog,
      openedShippingAddressEditDialog,
      openedShippingMethodEditDialog
    } = this.state;
    return (
      <Container width="md">
        <PageHeader
          className={classes.header}
          title={maybe(() => order.number) ? "#" + order.number : undefined}
          onBack={onBack}
        >
          <CardMenu
            className={classes.menu}
            menuItems={[
              {
                label: i18n.t("Cancel order", { context: "button" }),
                onSelect: onDraftRemove
              }
            ]}
          />
        </PageHeader>
        <div className={classes.date}>
          {order && order.created ? (
            <Typography variant="caption">
              <DateFormatter date={order.created} />
            </Typography>
          ) : (
            <Skeleton style={{ width: "10em" }} />
          )}
        </div>
        <div className={classes.root}>
          <div>
            <OrderDraftDetails
              order={order}
              onOrderLineAdd={onOrderLineAdd}
              onOrderLineChange={onOrderLineChange}
              onOrderLineRemove={onOrderLineRemove}
              onShippingMethodEdit={onShippingMethodEdit}
            />
            <OrderHistory
              history={maybe(() => order.events)}
              onNoteAdd={onNoteAdd}
            />
          </div>
          <div>
            <OrderCustomer
              canEditAddresses={true}
              canEditCustomer={true}
              order={order}
              users={users}
              loading={usersLoading}
              fetchUsers={fetchUsers}
              onBillingAddressEdit={onBillingAddressEdit}
              onCustomerEdit={onCustomerEdit}
              onShippingAddressEdit={onShippingAddressEdit}
            />
          </div>
        </div>
        <SaveButtonBar
          disabled={disabled || maybe(() => order.lines.length === 0)}
          onCancel={onBack}
          onSave={onDraftFinalize}
          labels={{ save: i18n.t("Finalize", { context: "button" }) }}
        />
      </Container>
    );
  }
}
const OrderDetailsPage = decorate<OrderDraftPageProps>(OrderDraftPageComponent);
export default OrderDetailsPage;
