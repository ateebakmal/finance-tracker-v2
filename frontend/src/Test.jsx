import { useModal } from "./components/modal/ModalProvider";
import { MODALS } from "./components/modal/modal-types";
function Test() {
  const { openModal } = useModal();

  return (
    <div className="space-y-5">
      <button onClick={() => openModal(MODALS.CREATE_CATEGORY)}>
        Add Category
      </button>
    </div>
  );
}

export default Test;
