import CreateCategoryModal from "@/features/categories/CreateCategoryModal";
import AppModal from "./AppModal";
import DemoModal from "./DemoModal";
import { MODALS } from "./modal-types";
import { useModal } from "./ModalProvider";
import SelectProfilesModal from "./SelectProfilesModal";
import CreateTagModal from "@/features/tags/CreateTagModal";
import CreateProfileModal from "@/features/profiles/CreateProfileModal";

const MODAL_REGISTRY = {
  [MODALS.DEMO]: {
    title: "Hello",
    description: "A test sheet",
    content: DemoModal,
  },
  [MODALS.SWITCH_PROFILE]: {
    title: "Switch Profile",
    content: SelectProfilesModal,
  },
  [MODALS.CREATE_PROFILE]: {
    title: "Create Profile",
    content: CreateProfileModal,
  },
  [MODALS.CREATE_CATEGORY]: {
    getTitle: (p) => `New ${p?.type ?? "expense"} category`,
    content: CreateCategoryModal,
  },
  [MODALS.CREATE_TAG]: {
    getTitle: (p) => `New ${p?.type ?? "expense"} tag`,
    content: CreateTagModal,
  },
};

export default function ModalRenderer() {
  const { activeModal, modalProps, closeModal } = useModal();

  if (!activeModal) return null;

  const modalConfig = MODAL_REGISTRY[activeModal];

  if (!modalConfig) return null;

  const title = modalConfig.getTitle
    ? modalConfig.getTitle(modalProps)
    : modalConfig.title;

  const Content = modalConfig.content;

  return (
    <AppModal
      open
      onClose={closeModal}
      title={title}
      description={modalConfig.description}
      contentClassName={modalConfig.contentClassName}
    >
      <Content {...modalProps} onClose={closeModal} />
    </AppModal>
  );
}
